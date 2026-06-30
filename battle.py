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


def print_status(team, enemy):
    active = team.active
    print(f"lv.{active.level} {active.name:<12} {hp_bar(active.hp, active.max_hp)}")
    print(f"lv.{enemy.level} {enemy.name:<12} {hp_bar(enemy.hp, enemy.max_hp)}")

    bench = [m for i, m in enumerate(team.members) if i != team.active_index]
    if bench:
        bench_str = "  |  ".join(
            f"{m.name} lv.{m.level} ({m.hp}/{m.max_hp} HP)"
            + ("" if m.is_alive() else " [fainted]")
            for m in bench
        )
        print(f"  Bench: {bench_str}")


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


def show_team_status(team):
    print("\nYour team:")
    for i, m in enumerate(team.members):
        tag = " (active)" if i == team.active_index else ""
        status = "" if m.is_alive() else " [fainted]"
        print(f"  {i + 1}. lv.{m.level} {m.name}{tag}{status} {hp_bar(m.hp, m.max_hp)}")


def prompt_switch(team, forced=False):
    show_team_status(team)
    if not forced:
        print("  0. Cancel")

    while True:
        raw = input("> ").strip()
        try:
            choice = int(raw)
        except ValueError:
            print("Invalid input.")
            continue

        if choice == 0 and not forced:
            return False

        idx = choice - 1
        if not (0 <= idx < len(team.members)):
            print("Invalid choice.")
            continue
        if idx == team.active_index:
            print("That monster is already active.")
            continue
        if not team.members[idx].is_alive():
            print("That monster has fainted and can't fight.")
            continue

        team.switch_to(idx)
        print(f"\nGo, {team.active.name}!")
        return True


def team_level_up(team):
    print("\nYour whole team gains experience!")
    team.level_up_all()


def check_fainted(team, enemy):
    if not enemy.is_alive():
        print(f"\n{enemy.name} fainted!")
        team_level_up(team)
        print(f"You win against {enemy.name}!")
        return True

    if not team.active.is_alive():
        print(f"\n{team.active.name} fainted!")
        if not team.is_alive():
            print("All your monsters have fainted! You lost!")
            return True
        print("Choose your next monster:")
        prompt_switch(team, forced=True)

    return False


def battle(team, enemy):
    enemy.defense_stage = enemy.attack_stage = 0
    for member in team.members:
        member.defense_stage = getattr(member, "defense_stage", 0)
        member.attack_stage  = getattr(member, "attack_stage",  0)

    if getattr(team.active, "relics", None):
        trigger_hook(team.active, enemy, "on_battle_start")

    print(f"\nA wild {enemy.name} appeared!")
    display_relics(team.active)

    while team.is_alive() and enemy.is_alive():
        player = team.active
        print("\n" + "-" * 40)
        print_status(team, enemy)
        print("-" * 40 + "\nChoose a move (or 'S' to switch monster):")

        for i, move in enumerate(player.moves, start=1):
            label = MOVE_LABELS.get(move.effect, f"(power: {move.power})")
            print(f"  {i}. {move.name} {label}")
        print("  S. Switch monster")

        raw = input("> ").strip()

        if raw.lower() == "s":
            if len(team.members) == 1:
                print("\nYou don't have any other monsters to switch to!")
                continue
            switched = prompt_switch(team)
            if not switched:
                continue

            # When switch enemy deals dmg (lose turn)
            new_player = team.active
            enemy_move = random.choice(enemy.moves)
            apply_move(enemy, new_player, enemy_move)
            if check_fainted(team, enemy):
                break
            if getattr(team.active, "relics", None):
                trigger_hook(team.active, enemy, "on_turn_end")
            if check_fainted(team, enemy):
                break
            continue

        try:
            choice = int(raw) - 1
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
        if check_fainted(team, enemy):
            break

        if second.is_alive():
            apply_move(second, first, second_move)

        if getattr(team.active, "relics", None):
            trigger_hook(team.active, enemy, "on_turn_end")

        if check_fainted(team, enemy):
            break