import random


PATH_TYPES = {
    "battle": {
        "label": "⚔ Battle",
        "desc":  "Fight a normal enemy. Standard rewards.",
    },
    "elite": {
        "label": "☠ Elite Battle",
        "desc":  "Face a stronger foe. Better rewards + relic chance.",
    },
    "campfire": {
        "label": "▲ Campfire",
        "desc":  "Rest and recover. Maybe find a small bonus.",
    },
    "mystery": {
        "label": "◈ Mystery Event",
        "desc":  "Something unexpected awaits...",
    },
}

# Weighted pool for random path generation
_PATH_WEIGHTS = {
    "battle":   40,
    "elite":    20,
    "campfire": 20,
    "mystery":  20,
}


def _weighted_choice(exclude=None):
    pool = {k: v for k, v in _PATH_WEIGHTS.items() if k != exclude}
    keys = list(pool.keys())
    weights = [pool[k] for k in keys]
    return random.choices(keys, weights=weights, k=1)[0]


def generate_path_choices(n=3):
    choices = ["battle"] # always offer one battle
    while len(choices) < n:
        pick = _weighted_choice()
        if pick not in choices:
            choices.append(pick)
    random.shuffle(choices)
    return choices


def choose_path():
    options = generate_path_choices(n=3)

    print("\n" + "=" * 42)
    print("            CHOOSE YOUR PATH")
    print("=" * 42)

    for i, key in enumerate(options, start=1):
        pt = PATH_TYPES[key]
        print(f"  {i}. {pt['label']}")
        print(f"     {pt['desc']}")

    print()
    while True:
        try:
            choice = int(input("> ")) - 1
            if 0 <= choice < len(options):
                chosen = options[choice]
                print(f"\nYou chose: {PATH_TYPES[chosen]['label']}")
                return chosen
            print(f"Pick 1–{len(options)}.")
        except ValueError:
            print("Invalid input.")


# Campfire logic

def do_campfire(player):
    """Campfire node: heal + optional bonus choice."""
    print("\n╔══════════════════════════════╗")
    print("║          CAMPFIRE            ║")
    print("╚══════════════════════════════╝")
    print("You sit by a warm fire and catch your breath.")

    # Base heal
    base_heal = int(player.max_hp * 0.30)
    gained = min(base_heal, player.max_hp - player.hp)
    player.hp += gained
    print(f"\nRestored {gained} HP. ({player.hp}/{player.max_hp})")

    # Optional bonus (50% chance)
    if random.random() < 0.5:
        bonus = random.choice(["atk", "def", "max_hp"])
        if bonus == "atk":
            player.attack += 1
            print("A traveler's note boosts your technique. ATK +1.")
        elif bonus == "def":
            player.defense += 1
            print("You sharpen your guard by the fire. DEF +1.")
        else:
            player.max_hp += 5
            player.hp = min(player.max_hp, player.hp + 5)
            print("The rest does wonders. Max HP +5.")
    else:
        print("The fire crackles quietly. No bonus tonight.")