import random
from relics import give_relic, random_relic_id


# ── Individual events ─────────────────────────────────────────────────────────

def event_strange_shrine(player):
    """Gain stats or sacrifice HP for a relic."""
    print("\n╔══════════════════════════════╗")
    print("║      STRANGE SHRINE          ║")
    print("╚══════════════════════════════╝")
    print("A glowing shrine pulses with energy.")
    print("  1. Pray (gain +1 ATK and +1 DEF - safe)")
    print("  2. Offer blood (sacrifice 20 HP for a random relic)")

    choice = _prompt_choice(2)
    if choice == 1:
        player.attack += 1
        player.defense += 1
        print(f"\nThe shrine blesses you. ATK and DEF each +1.")
    else:
        if player.hp <= 20:
            print("\nYou're too weak to survive the offering. You step back.")
            return
        player.hp -= 20
        print(f"\nYou bleed on the altar. ({player.hp}/{player.max_hp} HP)")
        relic_id = random_relic_id(player)
        if relic_id:
            give_relic(player, relic_id)
        else:
            print("The shrine has nothing left to give.")


def event_merchant(player):
    print("\n╔══════════════════════════════╗")
    print("║         MERCHANT             ║")
    print("╚══════════════════════════════╝")
    print("A hooded merchant eyes you carefully.")
    print("  1. Buy healing potion (costs 10 HP → restore 40 HP)")
    print("  2. Buy a random relic (costs 25 HP)")
    print("  3. Leave")

    choice = _prompt_choice(3)
    if choice == 1:
        if player.hp <= 10:
            print("\nYou can't afford that - not enough HP.")
        else:
            player.hp -= 10
            gained = min(40, player.max_hp - player.hp)
            player.hp += gained
            print(f"\nYou drink the potion and recover {gained} HP. ({player.hp}/{player.max_hp})")
    elif choice == 2:
        if player.hp <= 25:
            print("\nYou can't afford that - not enough HP.")
        else:
            player.hp -= 25
            print(f"\nYou pay the merchant. ({player.hp}/{player.max_hp} HP)")
            relic_id = random_relic_id(player)
            if relic_id:
                give_relic(player, relic_id)
            else:
                print("The merchant shrugs. No relics left.")
    else:
        print("\nYou walk away.")


def event_ancient_fountain(player):
    print("\n╔══════════════════════════════╗")
    print("║      ANCIENT FOUNTAIN        ║")
    print("╚══════════════════════════════╝")
    print("Crystal-clear water bubbles up from ancient stone.")
    print("  1. Drink (heal 30 HP)")
    print("  2. Bathe  (gain +10 Max HP, heal 10 HP)")

    choice = _prompt_choice(2)
    if choice == 1:
        gained = min(30, player.max_hp - player.hp)
        player.hp += gained
        print(f"\nYou feel refreshed. Healed {gained} HP. ({player.hp}/{player.max_hp})")
    else:
        player.max_hp += 10
        player.hp = min(player.max_hp, player.hp + 10)
        print(f"\nYou feel stronger. Max HP +10. ({player.hp}/{player.max_hp})")


def event_treasure_chest(player):
    print("\n╔══════════════════════════════╗")
    print("║       TREASURE CHEST         ║")
    print("╚══════════════════════════════╝")
    print("A dusty chest sits in the middle of the road...")
    input("Press Enter to open it...")

    roll = random.random()
    if roll < 0.35:
        gained = min(40, player.max_hp - player.hp)
        player.hp += gained
        print(f"\nA healing vial! Restored {gained} HP. ({player.hp}/{player.max_hp})")
    elif roll < 0.60:
        player.attack += 1
        print(f"\nA worn blade. Your attack permanently +1.")
    elif roll < 0.80:
        player.defense += 1
        print(f"\nA sturdy shield fragment. Your defense permanently +1.")
    else:
        relic_id = random_relic_id(player)
        if relic_id:
            print("\nA relic gleams inside!")
            give_relic(player, relic_id)
        else:
            player.max_hp += 5
            player.hp = min(player.max_hp, player.hp + 5)
            print("\nA peculiar gem. Max HP +5.")


def event_cursed_altar(player):
    print("\n╔══════════════════════════════╗")
    print("║       CURSED ALTAR           ║")
    print("╚══════════════════════════════╝")
    print("Dark energy radiates from a cracked obsidian altar.")
    print("  1. Gamble (50% chance: relic + 10 HP | 50% chance: lose 30 HP)")
    print("  2. Walk away (nothing happens)")

    choice = _prompt_choice(2)
    if choice == 2:
        print("\nWisdom sometimes looks like cowardice.")
        return

    if random.random() < 0.5:
        print("\nThe altar accepts you!")
        relic_id = random_relic_id(player)
        if relic_id:
            give_relic(player, relic_id)
        player.hp = min(player.max_hp, player.hp + 10)
        print(f"Healed 10 HP. ({player.hp}/{player.max_hp})")
    else:
        damage = min(30, player.hp - 1)  # can't kill with this alone
        player.hp -= damage
        print(f"\nThe altar rejects you! Lost {damage} HP. ({player.hp}/{player.max_hp})")


def event_wandering_healer(player):
    print("\n╔══════════════════════════════╗")
    print("║     WANDERING HEALER         ║")
    print("╚══════════════════════════════╝")
    print("A kind stranger patches your wounds.")
    gained = min(25, player.max_hp - player.hp)
    player.hp += gained
    print(f"\nHealed {gained} HP. ({player.hp}/{player.max_hp})")


def event_old_library(player):
    print("\n╔══════════════════════════════╗")
    print("║        OLD LIBRARY           ║")
    print("╚══════════════════════════════╝")
    print("You find a tome of ancient battle techniques.")
    print("  1. Study offense (+2 ATK)")
    print("  2. Study defense (+2 DEF)")
    print("  3. Study vitality (+8 Max HP, heal 8)")

    choice = _prompt_choice(3)
    if choice == 1:
        player.attack += 2
        print(f"\nYour strikes grow sharper. ATK +2.")
    elif choice == 2:
        player.defense += 2
        print(f"\nYou learn to absorb blows. DEF +2.")
    else:
        player.max_hp += 8
        player.hp = min(player.max_hp, player.hp + 8)
        print(f"\nYour body hardens. Max HP +8. ({player.hp}/{player.max_hp})")


# Event pool

EVENT_POOL = [
    event_strange_shrine,
    event_merchant,
    event_ancient_fountain,
    event_treasure_chest,
    event_cursed_altar,
    event_wandering_healer,
    event_old_library,
]

def run_event(player):
    event_fn = random.choice(EVENT_POOL)
    event_fn(player)

def _prompt_choice(max_choice):
    while True:
        try:
            val = int(input("> "))
            if 1 <= val <= max_choice:
                return val
            print(f"Enter a number between 1 and {max_choice}.")
        except ValueError:
            print("Invalid input.")