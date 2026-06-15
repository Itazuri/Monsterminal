from battle import battle
from creature import Creature
from moves import MOVES
from rewards import offer_rewards
import random


# Player

def create_player():
    return Creature(
        "FireKitty",
        hp=60,
        attack=6,
        defense=7,
        moves=[
            MOVES["fire_bite"],
            MOVES["armor_break"]
        ]
    )


# Enemies

enemy_templates = [
    ("FlamingFox",  50, 5, 4, ["fire_bite", "tackle"]),
    ("TankyFish", 55, 4, 6, ["water_splash", "wave_crash"]),
]


def create_enemy():
    name, hp, atk, def_, move_keys = random.choice(enemy_templates)
    return Creature(
        name,
        hp=hp,
        attack=atk,
        defense=def_,
        moves=[MOVES[m] for m in move_keys]
    )


# Game loop

def run_game():
    print("\nNEW RUN STARTED\n")

    player = create_player()

    for stage in range(3):
        print(f"\nStage {stage + 1}")

        enemy = create_enemy()

        battle(player, enemy)

        if not player.is_alive():
            print("\nYou lost the run.")
            return

        offer_rewards(player)

    # 1st Boss

    print("\nFINAL BOSS")

    boss = Creature(
        "TheBoss",
        hp=70,
        attack=8,
        defense=6,
        moves=[MOVES["fire_bite"], MOVES["wave_crash"]]
    )

    battle(player, boss)

    if player.is_alive():
        print("\nYou beat the game!! (for now)")
    else:
        print("\nYou lost!")


if __name__ == "__main__":
    run_game()