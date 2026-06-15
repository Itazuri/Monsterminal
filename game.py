from battle import battle
from creature import Creature
from moves import MOVES
import random


# ---------- PLAYER ----------

def create_player():
    return Creature(
        "FireKitty",
        hp=60,
        attack=6,
        defense=5,
        moves=[
            MOVES["fire_bite"],
            MOVES["armor_break"]
        ]
    )


# ---------- ENEMY TEMPLATES ----------

enemy_templates = [
    ("Flarefox",  50, 5, 4, ["fire_bite", "tackle"]),
    ("Aquabeast", 55, 4, 6, ["water_splash", "wave_crash"]),
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


# ---------- GAME LOOP ----------

def run_game():
    print("\n=== NEW RUN STARTED ===\n")

    player = create_player()

    for stage in range(3):
        print(f"\n--- Stage {stage + 1} ---")

        enemy = create_enemy()

        battle(player, enemy)

        if not player.is_alive():
            print("\nYou lost the run.")
            return

        print("\nReward: Rest or continue")
        choice = input("(r = rest +30 HP, c = continue): ").lower()

        if choice == "r":
            player.hp = min(player.max_hp, player.hp + 30)
            player.reset_combat_stats()
            print("Recovered 30 HP. (Stat stages reset)")
        # on continue: player stat stages carry over

    # ---------- BOSS ----------

    print("\nFINAL BOSS")

    boss = Creature(
        "BossFlare",
        hp=70,
        attack=8,
        defense=6,
        moves=[MOVES["fire_bite"], MOVES["wave_crash"]]
    )

    battle(player, boss)

    if player.is_alive():
        print("\nYOU WON THE RUN!")
    else:
        print("\nYOU LOST THE RUN!")


# ---------- ENTRY POINT ----------

if __name__ == "__main__":
    run_game()