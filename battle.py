import random
from moves import MOVES


def get_stage_multiplier(stage):
    stage = max(-6, min(6, stage))
    if stage >= 0:
        return (2 + stage) / 2
    else:
        return 2 / (2 - stage)


def calculate_damage(attacker, defender, move):
    atk = attacker.attack * get_stage_multiplier(attacker.attack_stage)
    def_ = defender.defense * get_stage_multiplier(defender.defense_stage)
    return max(1, int((move.power * atk) / def_))


def apply_move(user, target, move):

    # ---------- EFFECT SYSTEM ----------
    if move.effect == "defense_down":
        target.defense_stage = max(-6, target.defense_stage - 1)
        print(f"\n{target.name}'s defense fell!")
        return

    if move.effect == "attack_up":
        user.attack_stage = min(6, user.attack_stage + 1)
        print(f"\n{user.name}'s attack rose!")
        return

    # default = damage
    damage = calculate_damage(user, target, move)
    target.hp -= damage

    print(f"\n{user.name} used {move.name}!")
    print(f"{target.name} took {damage} damage!")


def battle(player, enemy):
    enemy.defense_stage = 0
    enemy.attack_stage = 0
    print(f"\nA wild {enemy.name} appeared!")

    while player.is_alive() and enemy.is_alive():

        print("\n------------------")
        print(f"{player.name}: {player.hp}/{player.max_hp} HP")
        print(f"{enemy.name}: {enemy.hp}/{enemy.max_hp} HP")
        print("------------------")

        print("\nChoose a move:")

        for i, move in enumerate(player.moves, start=1):
            if move.effect == "defense_down":
                print(f"{i}. {move.name} (lowers defense)")
            else:
                print(f"{i}. {move.name} (power: {move.power})")

        try:
            choice = int(input("> ")) - 1
        except ValueError:
            print("Invalid input!")
            continue

        if choice < 0 or choice >= len(player.moves):
            print("Invalid move!")
            continue

        move = player.moves[choice]

        # ---------- PLAYER TURN ----------
        apply_move(player, enemy, move)

        if not enemy.is_alive():
            print(f"\n{enemy.name} fainted!")
            print("You win!")
            break

        # ---------- ENEMY TURN ----------
        enemy_move = random.choice(enemy.moves)

        apply_move(enemy, player, enemy_move)

        if not player.is_alive():
            print(f"\n{player.name} fainted!")
            print("You lost!")
            break