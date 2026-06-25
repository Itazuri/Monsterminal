import random
from relics import give_relic, random_relic_id

def _heal_apply(p, frac):
    p.hp = min(p.max_hp, p.hp + max(1, int(p.max_hp * frac)))

def _max_hp_apply(p, frac):
    bonus = max(2, int(p.max_hp * frac))
    p.max_hp += bonus
    p.hp = min(p.max_hp, p.hp + bonus)

_HEAL_OPTIONS = [
    {
        "id": "heal_sm",
        "label": "Recover ~25% HP",
        "apply": lambda p: _heal_apply(p, 0.25),
    },
    {
        "id": "heal_md",
        "label": "Recover ~35% HP",
        "apply": lambda p: _heal_apply(p, 0.35),
    },
    {
        "id": "heal_max",
        "label": "+10% Max HP (and heal that amount)",
        "apply": lambda p: _max_hp_apply(p, 0.10),
    },
]

_STAT_OPTIONS = [
    {
        "id": "atk_up",
        "label": "+1 Attack (permanent)",
        "apply": lambda p: setattr(p, "attack", p.attack + 1),
    },
    {
        "id": "def_up",
        "label": "+1 Defense (permanent)",
        "apply": lambda p: setattr(p, "defense", p.defense + 1),
    },
    {
        "id": "keep_boosts",
        "label": "Keep combat ATK/DEF boosts from this fight",
        "apply": lambda p: None,
    },
]

# Elite reward options
ELITE_REWARD_POOL = [
    {
        "id": "atk_up2",
        "label": "+2 Attack (whole run)",
        "apply": lambda player: setattr(player, "attack", player.attack + 2)
    },
    {
        "id": "def_up2",
        "label": "+2 Defense (whole run)",
        "apply": lambda player: setattr(player, "defense", player.defense + 2)
    },
    {
        "id": "max_hp_up2",
        "label": "+15% Max HP (and heal that amount)",
        "apply": lambda player: _max_hp_apply(player, 0.15)
    },
]


def _pick_options(pool, n=2):
    return random.sample(pool, min(n, len(pool)))


def _apply_reward(player, options):
    for i, reward in enumerate(options, start=1):
        print(f"  {i}. {reward['label']}")

    while True:
        try:
            choice = int(input("> ")) - 1
            if 0 <= choice < len(options):
                break
            print(f"Pick 1–{len(options)}.")
        except ValueError:
            print("Invalid input.")

    chosen = options[choice]
    if chosen["id"] != "keep_boosts":
        player.reset_combat_stats()
    chosen["apply"](player)
    print(f"\nYou chose: {chosen['label']}")
    return chosen


def offer_rewards(player):
    heal_opt = random.choice(_HEAL_OPTIONS)
    stat_opt, stat_opt2 = random.sample(_STAT_OPTIONS, 2)
    options = [heal_opt, stat_opt, stat_opt2]
    random.shuffle(options)

    # reset boosts now unless they pick "keep_boosts"
    print("\n╔══════════════════════════════╗")
    print("║       CHOOSE A REWARD        ║")
    print("╚══════════════════════════════╝")
    _apply_reward(player, options)


def offer_elite_rewards(player):
    options = _pick_options(ELITE_REWARD_POOL, n=2)

    # 60% chance to also offer a relic
    relic_id = random_relic_id(player)
    if relic_id and random.random() < 0.60:
        from relics import get_relic
        relic = get_relic(relic_id)
        relic_option = {
            "id": f"relic_{relic_id}",
            "label": f"Relic: {relic['name']} — {relic['description']}",
            "apply": lambda p, rid=relic_id: give_relic(p, rid)
        }
        options.append(relic_option)

    if not any(r["id"] == "keep_boosts" for r in options):
        player.reset_combat_stats()

    print("\n╔══════════════════════════════╗")
    print("║    ELITE REWARD - CHOOSE     ║")
    print("╚══════════════════════════════╝")
    _apply_reward(player, options)