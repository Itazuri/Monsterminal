import random


def get_stage_multiplier(stage):
    stage = max(-6, min(6, stage))

    if stage >= 0:
        return (2 + stage) / 2
    else:
        return 2 / (2 - stage)


def calculate_damage(attacker, defender, move):
    atk = attacker.attack * get_stage_multiplier(attacker.attack_stage)
    def_ = defender.defense * get_stage_multiplier(defender.defense_stage)

    def_ = max(1, def_)

    return max(1, int((move.power * atk) / def_))


def hp_bar(hp, max_hp, length=20):
    hp = max(0, hp)
    filled = int((hp / max_hp) * length)
    bar = "█" * filled + "░" * (length - filled)
    return f"[{bar}] {hp}/{max_hp} HP"


def print_status(player, enemy):
    print(f"\nlv.{player.level} {player.name:<12} {hp_bar(player.hp, player.max_hp)}")
    print(f"{enemy.name:<16} {hp_bar(enemy.hp, enemy.max_hp)}")


# show its already maximum
def boost_stat(name, current, max_value=6):
    if current >= max_value:
        print(f"\n{name} is already at maximum!")
        return current, False
    return current + 1, True


def apply_move(user, target, move):

    if move.effect == "defense_down":
        target.defense_stage = max(-6, target.defense_stage - 1)
        print(f"\n{target.name}'s defense fell!")
        return

    if move.effect == "attack_up":
        user.attack_stage, changed = boost_stat(f"{user.name}'s attack", user.attack_stage)

        if changed:
            print(f"\n{user.name}'s attack rose!")
        return

    if move.effect == "defense_up":
        user.defense_stage, changed = boost_stat(f"{user.name}'s defense", user.defense_stage)

        if changed:
            print(f"\n{user.name}'s defense rose!")
        return

    damage = calculate_damage(user, target, move)
    target.hp -= damage
    target.hp = max(0, target.hp)

    print(f"\n{user.name} used {move.name}! {target.name} took {damage} damage.")


def battle(player, enemy):

    enemy.defense_stage = 0
    enemy.attack_stage = 0
    player.defense_stage = getattr(player, "defense_stage", 0)
    player.attack_stage = getattr(player, "attack_stage", 0)

    print(f"\nA wild {enemy.name} appeared!")

    while player.is_alive() and enemy.is_alive():

        print("\n" + "-" * 40)
        print_status(player, enemy)
        print("-" * 40)

        print("\nChoose a move:")

        for i, move in enumerate(player.moves, start=1):
            label = ""

            if move.effect == "defense_down":
                label = "(lowers enemy defense)"
            elif move.effect == "attack_up":
                label = "(raises your attack)"
            elif move.effect == "defense_up":
                label = "(raises your defense)"
            else:
                label = f"(power: {move.power})"

            print(f"  {i}. {move.name} {label}")

        try:
            choice = int(input("> ")) - 1
        except ValueError:
            print("Invalid input!")
            continue

        if choice < 0 or choice >= len(player.moves):
            print("Invalid move!")
            continue

        move = player.moves[choice]

        apply_move(player, enemy, move)

        if not enemy.is_alive():
            print(f"\n{enemy.name} fainted!")
            player.gain_xp(5)
            print(f"You win against {enemy.name}!")
            break

        enemy_move = random.choice(enemy.moves)
        apply_move(enemy, player, enemy_move)

        if not player.is_alive():
            print(f"\n{player.name} fainted! You lost!")
            break