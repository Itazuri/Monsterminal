import random
from relics import give_relic, random_relic_id

def _heal(player, fraction, label=None):
    amount = max(1, int(player.max_hp * fraction))
    gained = min(amount, player.max_hp - player.hp)
    player.hp += gained
    if label:
        print(f"\n{label} Healed {gained} HP. ({player.hp}/{player.max_hp})")
    return gained

def event_strange_shrine(player):
    print("\n╔══════════════════════════════╗")
    print("║      STRANGE SHRINE          ║")
    print("╚══════════════════════════════╝")
    print("A glowing shrine pulses with energy.")
    print("  1. Pray (gain +1 ATK and +1 DEF - safe)")
    cost = max(5, int(player.max_hp * 0.20))
    print(f"  2. Offer blood (sacrifice {cost} HP for a random relic)")

    choice = _prompt_choice(2)
    if choice == 1:
        player.attack += 1
        player.defense += 1
        print(f"\nThe shrine blesses you. ATK and DEF each +1.")
    else:
        if player.hp <= cost:
            print("\nYou're too weak to survive the offering. You step back.")
            return
        player.hp -= cost
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
    potion_cost = max(3, int(player.max_hp * 0.10))
    potion_heal = int(player.max_hp * 0.40)
    relic_cost  = max(8, int(player.max_hp * 0.25))
    print(f" 1. Buy healing potion (costs {potion_cost} HP → restore {potion_heal} HP)")
    print(f" 2. Buy a random relic (costs {relic_cost} HP)")
    print(" 3. Leave")

    choice = _prompt_choice(3)
    if choice == 1:
        if player.hp <= potion_cost:
            print("\nYou can't afford that, not enough HP.")
        else:
            player.hp -= potion_cost
            gained = min(potion_heal, player.max_hp - player.hp)
            player.hp += gained
            print(f"\nYou drink the potion and recover {gained} HP. ({player.hp}/{player.max_hp})")
    elif choice == 2:
        if player.hp <= relic_cost:
            print("\nYou can't afford that, not enough HP.")
        else:
            player.hp -= relic_cost
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
    drink_heal = int(player.max_hp * 0.35)
    bathe_bonus = max(4, int(player.max_hp * 0.10))
    print(f"  1. Drink (heal {drink_heal} HP)")
    print(f"  2. Bathe  (gain +{bathe_bonus} Max HP, heal {bathe_bonus} HP)")

    choice = _prompt_choice(2)
    if choice == 1:
        _heal(player, 0.35, "You feel refreshed.")
    else:
        player.max_hp += bathe_bonus
        player.hp = min(player.max_hp, player.hp + bathe_bonus)
        print(f"\nYou feel stronger. Max HP +{bathe_bonus}. ({player.hp}/{player.max_hp})")


def event_treasure_chest(player):
    print("\n╔══════════════════════════════╗")
    print("║       TREASURE CHEST         ║")
    print("╚══════════════════════════════╝")
    print("A dusty chest sits in the middle of the road...")
    input("Press Enter to open it...")

    roll = random.random()
    if roll < 0.35:
        _heal(player, 0.40, "A healing vial!")
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
            bonus = max(3, int(player.max_hp * 0.08))
            player.max_hp += bonus
            player.hp = min(player.max_hp, player.hp + bonus)
            print(f"\nA peculiar gem. Max HP +{bonus}.")


def event_cursed_altar(player):
    print("\n╔══════════════════════════════╗")
    print("║       CURSED ALTAR           ║")
    print("╚══════════════════════════════╝")
    print("Dark energy radiates from a cracked obsidian altar.")
    lose_hp  = max(5, int(player.max_hp * 0.30))
    gain_hp  = max(3, int(player.max_hp * 0.10))
    print(f" 1. Gamble (50%: relic + {gain_hp} HP | 50%: lose {lose_hp} HP)")
    print(" 2. Walk away (nothing happens)")

    choice = _prompt_choice(2)
    if choice == 2:
        print("\nWisdom sometimes looks like cowardice.")
        return

    if random.random() < 0.5:
        print("\nThe altar accepts you!")
        relic_id = random_relic_id(player)
        if relic_id:
            give_relic(player, relic_id)
        player.hp = min(player.max_hp, player.hp + gain_hp)
        print(f"Healed {gain_hp} HP. ({player.hp}/{player.max_hp})")
    else:
        damage = min(lose_hp, player.hp - 1)  # can't kill
        player.hp -= damage
        print(f"\nThe altar rejects you! Lost {damage} HP. ({player.hp}/{player.max_hp})")


def event_wandering_healer(player):
    print("\n╔══════════════════════════════╗")
    print("║     WANDERING HEALER         ║")
    print("╚══════════════════════════════╝")
    print("A kind stranger patches your wounds.")
    _heal(player, 0.30, "")
    print(f"({player.hp}/{player.max_hp})")


def event_old_library(player):
    print("\n╔══════════════════════════════╗")
    print("║        OLD LIBRARY           ║")
    print("╚══════════════════════════════╝")
    print("You find a tome of ancient battle techniques.")
    vit_bonus = max(4, int(player.max_hp * 0.10))
    print("  1. Study offense (+2 ATK)")
    print("  2. Study defense (+2 DEF)")
    print(f"  3. Study vitality (+{vit_bonus} Max HP, heal {vit_bonus})")

    choice = _prompt_choice(3)
    if choice == 1:
        player.attack += 2
        print(f"\nYour strikes grow sharper. ATK +2.")
    elif choice == 2:
        player.defense += 2
        print(f"\nYou learn to absorb blows. DEF +2.")
    else:
        player.max_hp += vit_bonus
        player.hp = min(player.max_hp, player.hp + vit_bonus)
        print(f"\nYour body hardens. Max HP +{vit_bonus}. ({player.hp}/{player.max_hp})")

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