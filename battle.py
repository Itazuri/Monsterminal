import random
from relics import trigger_hook, display_relics

MOVE_LABELS = {
    "defense_down": "(lowers enemy defense)",
    "attack_up":    "(raises your attack)",
    "defense_up":   "(raises your defense)",
}


def get_stage_multiplier(stage):
    stage = max(-6, min(6, stage))
    return (2 + stage) / 2 if stage >= 0 else 2 / (2 - stage)


def calculate_damage(attacker, defender, move):
    atk  = attacker.attack  * get_stage_multiplier(attacker.attack_stage)
    def_ = max(1, defender.defense * get_stage_multiplier(defender.defense_stage))
    return max(1, int((move.power * atk) / def_))


def hp_bar(hp, max_hp, length=20):
    filled = int((max(0, hp) / max_hp) * length)
    return f"[{'█' * filled}{'░' * (length - filled)}] {hp}/{max_hp} HP"


def print_status(player, enemy):
    for c in (player, enemy):
        print(f"lv.{c.level} {c.name:<12} {hp_bar(c.hp, c.max_hp)}")


def boost_stat(entity, attr):
    current = getattr(entity, attr)
    if current >= 6:
        print(f"\n{entity.name}'s {attr.replace('_stage', '')} is already at maximum!")
        return
    setattr(entity, attr, current + 1)
    print(f"\n{entity.name}'s {attr.replace('_stage', '')} rose!")


def apply_move(user, target, move):
    if move.effect == "defense_down":
        target.defense_stage = max(-6, target.defense_stage - 1)
        print(f"\n{user.name} hit {target.name} with {move.name} and it's defense fell!")
        return

    if move.effect == "attack_up":
        return boost_stat(user, "attack_stage")

    if move.effect == "defense_up":
        return boost_stat(user, "defense_stage")

    damage = calculate_damage(user, target, move)
    if getattr(user, "relics", None):
        damage = trigger_hook(user, target, "on_damage_dealt", damage=damage, move=move)

    target.hp = max(0, target.hp - damage)
    print(f"\n{user.name} used {move.name}! {target.name} took {damage} damage.")


def check_fainted(player, enemy):
    if not enemy.is_alive():
        print(f"\n{enemy.name} fainted!")
        player.level_up()  # Stat gains + new move if learnable
        print(f"You win against {enemy.name}!")
        return True
    if not player.is_alive():
        print(f"\n{player.name} fainted! You lost!")
        return True
    return False


def battle(player, enemy):
    enemy.defense_stage = enemy.attack_stage = 0
    player.defense_stage = getattr(player, "defense_stage", 0)
    player.attack_stage  = getattr(player, "attack_stage",  0)

    if getattr(player, "relics", None):
        trigger_hook(player, enemy, "on_battle_start")

    print(f"\nA wild {enemy.name} appeared!")
    display_relics(player)

    while player.is_alive() and enemy.is_alive():
        print("\n" + "-" * 40)
        print_status(player, enemy)
        print("-" * 40 + "\nChoose a move:")

        for i, move in enumerate(player.moves, start=1):
            label = MOVE_LABELS.get(move.effect, f"(power: {move.power})")
            print(f"  {i}. {move.name} {label}")

        try:
            choice = int(input("> ")) - 1
        except ValueError:
            print("Invalid input!")
            continue

        if not (0 <= choice < len(player.moves)):
            print("Invalid move!")
            continue

        move       = player.moves[choice]
        enemy_move = random.choice(enemy.moves)

        # Speed check, coinflip on tie
        player_first = player.speed > enemy.speed or (
            player.speed == enemy.speed and random.random() < 0.5
        )
        (first, first_move), (second, second_move) = (
            ((player, move), (enemy, enemy_move)) if player_first
            else ((enemy, enemy_move), (player, move))
        )

        if player.speed != enemy.speed:
            print(f"\n{first.name} is faster and goes first!")

        apply_move(first, second, first_move)
        if check_fainted(player, enemy):
            break

        apply_move(second, first, second_move)

        if getattr(player, "relics", None):
            trigger_hook(player, enemy, "on_turn_end")

        if check_fainted(player, enemy):
            break