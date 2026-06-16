import random
from relics import give_relic, random_relic_id


REWARD_POOL = [
    {
        "id": "continue",
        "label": "Continue (keep attack/defense boosts)",
        "apply": lambda player: None  # keep boosts
    },
    {
        "id": "atk_up",
        "label": "+1 Attack (whole run)",
        "apply": lambda player: setattr(player, "attack", player.attack + 1)
    },
    {
        "id": "def_up",
        "label": "+1 Defense (whole run)",
        "apply": lambda player: setattr(player, "defense", player.defense + 1)
    },
    {
        "id": "heal",
        "label": "Heal 35 HP",
        "apply": lambda player: setattr(player, "hp", min(player.max_hp, player.hp + 35))
    },
    {
        "id": "max_hp_up",
        "label": "+5 Max HP (and heal 5)",
        "apply": lambda player: (
            setattr(player, "max_hp", player.max_hp + 5),
            setattr(player, "hp", min(player.max_hp, player.hp + 5))
        )
    },
]

# Elite rewards
ELITE_REWARD_POOL = [
    {
        "id": "big_heal",
        "label": "Heal 60 HP",
        "apply": lambda player: setattr(player, "hp", min(player.max_hp, player.hp + 60))
    },
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
        "label": "+12 Max HP (and heal 12)",
        "apply": lambda player: (
            setattr(player, "max_hp", player.max_hp + 12),
            setattr(player, "hp", min(player.max_hp, player.hp + 12))
        )
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
    if chosen["id"] != "continue":
        player.reset_combat_stats()
    chosen["apply"](player)
    print(f"\nYou chose: {chosen['label']}")
    return chosen


def offer_rewards(player):
    options = _pick_options(REWARD_POOL, n=2)

    # reset combat stats if "continue" wasn't even offered
    if not any(r["id"] == "continue" for r in options):
        player.reset_combat_stats()

    print("\n╔══════════════════════════════╗")
    print("║       CHOOSE A REWARD        ║")
    print("╚══════════════════════════════╝")
    _apply_reward(player, options)


def offer_elite_rewards(player):
    options = _pick_options(ELITE_REWARD_POOL, n=2)

    # 60% chance to also offer a relic
    relic_id = random_relic_id(player)
    relic_option = None
    if relic_id and random.random() < 0.60:
        from relics import get_relic
        relic = get_relic(relic_id)
        relic_option = {
            "id": f"relic_{relic_id}",
            "label": f"Relic: {relic['name']} - {relic['description']}",
            "apply": lambda p, rid=relic_id: give_relic(p, rid)
        }
        options.append(relic_option)

    # reset combat stats if "continue" wasn't offered
    if not any(r["id"] == "continue" for r in options):
        player.reset_combat_stats()

    print("\n╔══════════════════════════════╗")
    print("║    ELITE REWARD - CHOOSE     ║")
    print("╚══════════════════════════════╝")
    _apply_reward(player, options)