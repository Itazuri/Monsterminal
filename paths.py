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
    """Campfire node: choose between healing OR a stat bonus — not both."""
    print("\n╔══════════════════════════════╗")
    print("║          CAMPFIRE            ║")
    print("╚══════════════════════════════╝")
    print("You sit by a warm fire. You can only focus on one thing tonight.\n")

    heal_amount = max(1, int(player.max_hp * 0.35))
    max_hp_bonus = max(3, int(player.max_hp * 0.10))

    bonus_type = random.choice(["atk", "def", "max_hp"])
    if bonus_type == "atk":
        bonus_label = "Study (+1 ATK)"
    elif bonus_type == "def":
        bonus_label = "Train (+1 DEF)"
    else:
        bonus_label = f"Meditate (+{max_hp_bonus} Max HP)"

    print(f"  1. Rest    (heal {heal_amount} HP)")
    print(f"  2. {bonus_label}")

    while True:
        try:
            choice = int(input("> "))
            if choice in (1, 2):
                break
            print("Enter 1 or 2.")
        except ValueError:
            print("Invalid input.")

    if choice == 1:
        gained = min(heal_amount, player.max_hp - player.hp)
        player.hp += gained
        print(f"\nYou sleep soundly. Restored {gained} HP. ({player.hp}/{player.max_hp})")
    else:
        if bonus_type == "atk":
            player.attack += 1
            print("\nYour strikes grow sharper by morning. ATK +1.")
        elif bonus_type == "def":
            player.defense += 1
            print("\nYou drill your guard through the night. DEF +1.")
        else:
            player.max_hp += max_hp_bonus
            player.hp = min(player.max_hp, player.hp + max_hp_bonus)
            print(f"\nDeep focus hardens your body. Max HP +{max_hp_bonus}. ({player.hp}/{player.max_hp})")