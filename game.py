import random
from battle import battle
from creature import Creature
from moves import MOVES
from rewards import offer_rewards, offer_elite_rewards
from relics import give_relic, display_relics, random_relic_id, get_relic
from events import run_event
from paths import choose_path, do_campfire


NUM_STAGES = 3   # Number of path nodes per act before the boss

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

# Enemy templates (name, hp, atk, def, speed, move_keys)

NORMAL_ENEMIES = [
    ("FlamingFox", 50, 5, 4,  7, ["fire_bite", "tackle"]),
    ("TankyFish", 55, 4, 6,  4, ["water_splash", "wave_crash"]),
    ("Rocky", 90, 1, 6,  2, ["harden"]),
    ("Nany", 10, 20, 3, 10, ["water_splash", "fire_bite"]),
]

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

# Enemy Scaling

def _enemy_level(act, offset_min, offset_max):
    return random.randint(act + offset_min, act + offset_max)


def create_normal_enemy(act=1):
    enemy = _make_enemy(random.choice(NORMAL_ENEMIES))
    lvl = _enemy_level(act, offset_min=0, offset_max=2)
    if lvl > 1:
        enemy.set_level(lvl)
    return enemy


def create_elite_enemy(act=1):
    enemy = _make_enemy(random.choice(ELITE_ENEMIES))
    lvl = _enemy_level(act, offset_min=1, offset_max=3)
    if lvl > 1:
        enemy.set_level(lvl)
    return enemy

# Bosses

def _make_boss_the_inferno(act):
    boss = Creature(
        "The Inferno",
        hp=90,
        attack=9,
        defense=7,
        speed=6,
        moves=[MOVES["fire_bite"], MOVES["wave_crash"], MOVES["armor_break"]]
    )
    lvl = _enemy_level(act, offset_min=2, offset_max=4)
    if lvl > 1:
        boss.set_level(lvl)
    return boss


def _make_boss_crystal_golem(act):
    boss = Creature(
        "Crystal Golem",
        hp=110,
        attack=7,
        defense=11,
        speed=3,
        moves=[MOVES["harden"], MOVES["wave_crash"], MOVES["armor_break"]]
    )
    lvl = _enemy_level(act, offset_min=2, offset_max=4)
    if lvl > 1:
        boss.set_level(lvl)
    return boss


# Bosses in Boss pool
BOSS_POOL = [
    _make_boss_the_inferno,
    _make_boss_crystal_golem,
]


def create_boss(act=1):
    make_fn = random.choice(BOSS_POOL)
    return make_fn(act)

# Act-clear reward

def _offer_act_clear_reward(player, act):
    print("\n" + "=" * 42)
    print(f"           ACT {act} CLEARED")
    print("=" * 42)
    print("Choose your reward:\n")

    options = []

    # Always offer a heal
    options.append({
        "label": "Heal 50 HP",
        "apply": lambda p: setattr(p, "hp", min(p.max_hp, p.hp + 50)),
    })

    # Always offer a relic if one is available, otherwise a stat boost
    relic_id = random_relic_id(player)
    if relic_id:
        relic = get_relic(relic_id)
        options.append({
            "label": f"Relic: {relic['name']} -- {relic['description']}",
            "apply": lambda p, rid=relic_id: give_relic(p, rid),
        })
    else:
        options.append({
            "label": "+2 Attack (permanent)",
            "apply": lambda p: setattr(p, "attack", p.attack + 2),
        })

    # Always offer a permanent stat upgrade
    stat_choice = random.choice(["atk", "def", "max_hp"])
    if stat_choice == "atk":
        options.append({
            "label": "+2 Attack (permanent)",
            "apply": lambda p: setattr(p, "attack", p.attack + 2),
        })
    elif stat_choice == "def":
        options.append({
            "label": "+2 Defense (permanent)",
            "apply": lambda p: setattr(p, "defense", p.defense + 2),
        })
    else:
        options.append({
            "label": "+15 Max HP (and heal 15)",
            "apply": lambda p: (
                setattr(p, "max_hp", p.max_hp + 15),
                setattr(p, "hp", min(p.max_hp, p.hp + 15)),
            ),
        })

    for i, opt in enumerate(options, start=1):
        print(f"  {i}. {opt['label']}")

    print()
    while True:
        try:
            choice = int(input("> ")) - 1
            if 0 <= choice < len(options):
                break
            print(f"Pick 1-{len(options)}.")
        except ValueError:
            print("Invalid input.")

    options[choice]["apply"](player)
    player.reset_combat_stats()
    print(f"\nYou chose: {options[choice]['label']}")

# Path resolution

def resolve_path(path_type, player, stage_num, act):

    if path_type == "battle":
        enemy = create_normal_enemy(act)
        battle(player, enemy)
        if not player.is_alive():
            return False
        offer_rewards(player)

    elif path_type == "elite":
        print("\n! An elite enemy blocks your path!")
        enemy = create_elite_enemy(act)
        battle(player, enemy)
        if not player.is_alive():
            return False
        offer_elite_rewards(player)

    elif path_type == "campfire":
        do_campfire(player)

    elif path_type == "mystery":
        run_event(player)

    return True

# Status display

def print_run_status(player, stage_num, act):
    print(f"\n{'─'*42}")
    print(f"  Act {act}  |  Stage {stage_num}/{NUM_STAGES}  |  "
          f"lv.{player.level} {player.name}")
    print(f"  HP {player.hp}/{player.max_hp}  |  "
          f"ATK {player.attack}  DEF {player.defense}")
    display_relics(player)
    print(f"{'─'*42}")

# Main run loop - endless acts

def run_game():
    print("\nNEW RUN STARTED\n")
    player = create_player()
    act = 1

    while True:

        # Act intro banner
        print("\n" + "=" * 42)
        print(f"              ACT {act}")
        print("=" * 42)

        # Path stages
        for stage in range(1, NUM_STAGES + 1):
            print_run_status(player, stage, act)

            path = choose_path()
            alive = resolve_path(path, player, stage, act)

            if not alive:
                print(f"\nYou fell in Act {act}, Stage {stage}.")
                return

        # Boss stage
        print("\n" + "=" * 42)
        print(f"         ACT {act} BOSS")
        print("=" * 42)
        print_run_status(player, "BOSS", act)

        boss = create_boss(act)
        battle(player, boss)

        if not player.is_alive():
            print(f"\nYou fell to the Act {act} Boss.")
            print(f"You made it to Act {act}. Well fought.")
            return
        # Act clear
        _offer_act_clear_reward(player, act)
        act += 1