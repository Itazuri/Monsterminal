import random
from battle import battle
from creature import Creature
from team import Team
from moves import MOVES
from rewards import offer_rewards, offer_elite_rewards
from relics import give_relic, display_relics, random_relic_id, get_relic
from events import run_event
from paths import choose_path, do_campfire
from monsters import make_normal_enemy, make_elite_enemy


NUM_STAGES = 3   # Number of path nodes per act before the boss


def create_starter():
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


def create_player_team():
    return Team(create_starter())


def create_normal_enemy(act=1):
    return make_normal_enemy(act)


def create_elite_enemy(act=1):
    return make_elite_enemy(act)


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
    lvl = random.randint((act - 1) * 4 + 4, (act - 1) * 4 + 5)
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
    lvl = random.randint((act - 1) * 4 + 4, (act - 1) * 4 + 5)
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


def _offer_act_clear_reward(team, act):
    player = team.active
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


def resolve_path(path_type, team, stage_num, act):
    if path_type == "battle":
        enemy = create_normal_enemy(act)
        battle(team, enemy)
        if not team.is_alive():
            return False
        offer_rewards(team.active)

    elif path_type == "elite":
        print("\n! An elite enemy blocks your path!")
        enemy = create_elite_enemy(act)
        battle(team, enemy)
        if not team.is_alive():
            return False
        offer_elite_rewards(team.active)

    elif path_type == "campfire":
        do_campfire(team.active)

    elif path_type == "mystery":
        run_event(team)

    return True


def print_run_status(team, stage_num, act):
    player = team.active
    print(f"\n{'─'*42}")
    print(f"  Act {act}  |  Stage {stage_num}/{NUM_STAGES}  |  "
          f"lv.{player.level} {player.name}")
    print(f"  HP {player.hp}/{player.max_hp}  |  "
          f"ATK {player.attack}  DEF {player.defense}  SPD {player.speed}")

    bench = [m for i, m in enumerate(team.members) if i != team.active_index]
    if bench:
        bench_str = "  |  ".join(f"lv.{m.level} {m.name} ({m.hp}/{m.max_hp} HP)" for m in bench)
        print(f"  Team: {bench_str}")

    display_relics(player)
    print(f"{'─'*42}")


def run_game():
    print("\nNEW RUN STARTED\n")
    team = create_player_team()
    act = 1

    while True:
        print("\n" + "=" * 42)
        print(f"              ACT {act}")
        print("=" * 42)

        for stage in range(1, NUM_STAGES + 1):
            print_run_status(team, stage, act)
            path = choose_path()
            alive = resolve_path(path, team, stage, act)
            if not alive:
                print(f"\nYou fell in Act {act}, Stage {stage}.")
                return

        print("\n" + "=" * 42)
        print(f"         ACT {act} BOSS")
        print("=" * 42)
        print_run_status(team, "BOSS", act)

        boss = create_boss(act)
        battle(team, boss)

        if not team.is_alive():
            print(f"\nYou fell to the Act {act} Boss.")
            return

        _offer_act_clear_reward(team, act)
        act += 1