import random


REWARD_POOL = [
    {
        "id": "continue",
        "label": "Continue (keep attack/defense boosts)",
        "apply": lambda player: None  # keep boosts
    },
    {
        "id": "atk_up",
        "label": "+1 Attack (permanent)",
        "apply": lambda player: setattr(player, "attack", player.attack + 1)
    },
    {
        "id": "def_up",
        "label": "+1 Defense (permanent)",
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


def offer_rewards(player):
    options = random.sample(REWARD_POOL, 2)

    # reset if continue is not offered
    if not any(r["id"] == "continue" for r in options):
        player.reset_combat_stats()

    print("\n--- CHOOSE A REWARD ---")
    for i, reward in enumerate(options, start=1):
        print(f"{i}. {reward['label']}")

    while True:
        try:
            choice = int(input("> ")) - 1
            if 0 <= choice < len(options):
                break
            print("Pick 1 or 2.")
        except ValueError:
            print("Invalid input.")

    chosen = options[choice]

    # reset if continue not chosen
    if chosen["id"] != "continue":
        player.reset_combat_stats()

    chosen["apply"](player)
    print(f"\nYou chose: {chosen['label']}")