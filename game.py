import random
from battle import battle
from creature import Creature
from moves import MOVES
from rewards import offer_rewards, offer_elite_rewards
from relics import give_relic, display_relics, random_relic_id, get_relic
from events import run_event
from paths import choose_path, do_campfire


NUM_STAGES = 3   # Number of path nodes per act before the boss

def create_player():
    return Creature(
        "FireKitty",
        hp=80,
        attack=8,
        defense=8,
        speed=8,
        move_pool=[
            (1,  MOVES["fire_bite"]),
            (1,  MOVES["harden"]),
            (2,  MOVES["sharpen"]),
            (3,  MOVES["armor_break"]),
            (7,  MOVES["fire_storm"]),
        ]
    )

NORMAL_ENEMIES = [
    #  name          hp   atk  def  spd
    ("FlamingFox", 65, 7, 5, 9 [
        (1,  "tackle"),
        (2,  "fire_bite"),
        (10, "fire_storm"),
    ]),
    ("TankyFish", 75, 5, 8, 4 [
        (1,  "water_splash"),
        (3,  "wave_crash"),
        (4,  "harden"),
    ]),
    ("Rocky", 100, 4, 8, 2 [
        (1,  "harden"),
    ]),
    ("Nany", 30, 14, 3, 12 [
        (1,  "water_splash"),
        (2,  "fire_bite"),
    ]),
]

ELITE_ENEMIES = [
    ("Infernum", 90, 10, 6, 9 [
        (1,  "fire_bite"),
        (2,  "tackle"),
        (4,  "wave_crash"),
        (5,  "armor_break"),
        (14, "fire_storm"),
    ]),
    ("SteelCrab", 95, 6, 12, 3 [
        (1,  "harden"),
        (2,  "tackle"),
        (5,  "armor_break"),
    ]),
    ("DarkShadow", 80, 11, 5, 11 [
        (1,  "fire_bite"),
        (3,  "armor_break"),
        (5,  "sharpen"),
    ]),
    ("Leviathan", 100, 9, 7, 5 [
        (1,  "water_splash"),
        (2,  "wave_crash"),
        (4,  "harden"),
    ]),
]


def _make_enemy(template):
    name, hp, atk, def_, spd, pool = template
    return Creature(
        name, hp=hp, attack=atk, defense=def_, speed=spd,
        move_pool=[(lvl, MOVES[key]) for lvl, key in pool]
    )

def _enemy_level(act, offset_min, offset_max):
    base = (act - 1) * 4
    return random.randint(base + offset_min, base + offset_max)


def create_normal_enemy(act=1):
    enemy = _make_enemy(random.choice(NORMAL_ENEMIES))
    lvl = _enemy_level(act, offset_min=1, offset_max=3)
    if lvl > 1:
        enemy.set_level(lvl)
    return enemy


def create_elite_enemy(act=1):
    enemy = _make_enemy(random.choice(ELITE_ENEMIES))
    lvl = _enemy_level(act, offset_min=3, offset_max=5)
    if lvl > 1:
        enemy.set_level(lvl)
    return enemy

def _make_boss_the_inferno(act):
    boss = Creature(
        "The Inferno",
        hp=110,
        attack=11,
        defense=8,
        speed=7,
        move_pool=[
            (1,  MOVES["fire_bite"]),
            (2,  MOVES["tackle"]),
            (3,  MOVES["armor_break"]),
            (17, MOVES["fire_storm"]),
        ]
    )
    lvl = _enemy_level(act, offset_min=4, offset_max=5)
    if lvl > 1:
        boss.set_level(lvl)
    return boss


def _make_boss_crystal_golem(act):
    boss = Creature(
        "Crystal Golem",
        hp=135,
        attack=8,
        defense=14,
        speed=3,
        move_pool=[
            (1,  MOVES["harden"]),
            (2,  MOVES["tackle"]),
            (3,  MOVES["armor_break"]),
            (5,  MOVES["wave_crash"]),
        ]
    )
    lvl = _enemy_level(act, offset_min=4, offset_max=5)
    if lvl > 1:
        boss.set_level(lvl)
    return boss


BOSS_POOL = [
    _make_boss_the_inferno,
    _make_boss_crystal_golem,
]


def create_boss(act=1):
    make_fn = random.choice(BOSS_POOL)
    return make_fn(act)

def _offer_act_clear_reward(player, act):
    print("\n" + "=" * 42)
    print(f"           ACT {act} CLEARED")
    print("=" * 42)
    print("Choose your reward:\n")

    options = []

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

def print_run_status(player, stage_num, act):
    print(f"\n{'─'*42}")
    print(f"  Act {act}  |  Stage {stage_num}/{NUM_STAGES}  |  "
          f"lv.{player.level} {player.name}")
    print(f"  HP {player.hp}/{player.max_hp}  |  "
          f"ATK {player.attack}  DEF {player.defense}  SPD {player.speed}")
    display_relics(player)
    print(f"{'─'*42}")

def run_game():
    print("\nNEW RUN STARTED\n")
    player = create_player()
    act = 1

    while True:
        print("\n" + "=" * 42)
        print(f"              ACT {act}")
        print("=" * 42)

        for stage in range(1, NUM_STAGES + 1):
            print_run_status(player, stage, act)
            path = choose_path()
            alive = resolve_path(path, player, stage, act)
            if not alive:
                print(f"\nYou fell in Act {act}, Stage {stage}.")
                return

        print("\n" + "=" * 42)
        print(f"         ACT {act} BOSS")
        print("=" * 42)
        print_run_status(player, "BOSS", act)

        boss = create_boss(act)
        battle(player, boss)

        if not player.is_alive():
            print(f"\nYou fell to the Act {act} Boss.")
            return

        _offer_act_clear_reward(player, act)
        act += 1