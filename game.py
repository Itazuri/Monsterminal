from battle import battle
from creature import Creature
from moves import MOVES
from rewards import offer_rewards, offer_elite_rewards
from relics import give_relic, display_relics
from events import run_event
from paths import choose_path, do_campfire
import random

NUM_STAGES = 3   # Number of paths before boss


# Player

def create_player():
    return Creature(
        "FireKitty",
        hp=60,
        attack=6,
        defense=7,
        speed=8,
        moves=[
            MOVES["fire_bite"],
            MOVES["armor_break"],
            MOVES["harden"],
            MOVES["sharpen"]
        ]
    )


# Enemy Templates

# (name, hp, atk, def, speed, move_keys)
NORMAL_ENEMIES = [
    ("FlamingFox", 50, 5, 4,  7, ["fire_bite", "tackle"]),
    ("TankyFish", 55, 4, 6,  4, ["water_splash", "wave_crash"]),
    ("Rocky", 90, 1, 6,  2, ["harden"]),
    ("Nany", 10, 20, 3, 10, ["water_splash", "fire_bite"]),
]

# Elites are stronger
ELITE_ENEMIES = [
    ("Infernum", 75, 8, 5,  8, ["fire_bite", "wave_crash"]),
    ("SteelCrab", 80, 5, 9,  3, ["harden", "tackle"]),
    ("DarkShadow", 65, 9, 4, 10, ["fire_bite", "armor_break"]),
    ("Leviathan", 85, 7, 6,  5, ["wave_crash", "water_splash"]),
]


def _make_enemy(template):
    name, hp, atk, def_, spd, move_keys = template
    return Creature(
        name, hp=hp, attack=atk, defense=def_, speed=spd,
        moves=[MOVES[m] for m in move_keys]
    )


def create_normal_enemy():
    return _make_enemy(random.choice(NORMAL_ENEMIES))


def create_elite_enemy():
    return _make_enemy(random.choice(ELITE_ENEMIES))


def create_boss():
    return Creature(
        "TheBoss",
        hp=90,
        attack=9,
        defense=7,
        speed=6,
        moves=[MOVES["fire_bite"], MOVES["wave_crash"], MOVES["armor_break"]]
    )


# Path resolution

def resolve_path(path_type, player, stage_num):

    if path_type == "battle":
        enemy = create_normal_enemy()
        battle(player, enemy)
        if not player.is_alive():
            return False
        offer_rewards(player)

    elif path_type == "elite":
        print("\n⚠ An elite enemy blocks your path!")
        enemy = create_elite_enemy()
        battle(player, enemy)
        if not player.is_alive():
            return False
        offer_elite_rewards(player)

    elif path_type == "campfire":
        do_campfire(player)

    elif path_type == "mystery":
        run_event(player)

    return True


# Status Display

def print_run_status(player, stage_num):
    print(f"\n{'─'*42}")
    print(f"  Stage {stage_num}/{NUM_STAGES}  |  "
          f"lv.{player.level} {player.name}  |  "
          f"HP {player.hp}/{player.max_hp}  |  "
          f"ATK {player.attack}  DEF {player.defense}")
    display_relics(player)
    print(f"{'─'*42}")


# Main run loop

def run_game():
    print("\nNEW RUN STARTED\n")
    player = create_player()

    for stage in range(1, NUM_STAGES + 1):
        print_run_status(player, stage)

        path = choose_path()
        alive = resolve_path(path, player, stage)

        if not alive:
            print("\nYou lost the run.")
            return

    # Boss stage
    print("\n" + "=" * 42)
    print("           FINAL BOSS")
    print("=" * 42)
    print_run_status(player, "BOSS")

    boss = create_boss()
    battle(player, boss)

    if player.is_alive():
        print("\n🏆 You beat the game!! (for now)")
    else:
        print("\nYou lost to the Final Boss!")