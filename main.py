from game import run_game
import time
import os
import sys


def slow_print(text, delay=0.02):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def clear():
    os.system("clear")


def intro(animated=True):
    clear()

    print("\n")
    print("===================================")
    print("          MONSTERMINAL")
    print("   Terminal Creature Roguelike")
    print("===================================")

    if animated:
        slow_print("A turn-based monster battling roguelike")
        slow_print("built for the terminal.\n")
    else:
        print("A turn-based monster battling roguelike")
        print("built for the terminal.\n")

def how_to_play():
    print("\n           HOW TO PLAY\n")

    print("- Fight through stages of creatures")
    print("- Choose moves each turn")
    print("- Manage HP and defense buffs")
    print("- Reach and defeat the final boss")
    print("- Choose rewards after each fight\n")

    print("Rewards:")
    print("  • Heal")
    print("  • Continue (keep buffs)")
    print("  • Permanent stat upgrade\n")


def main_menu():
    first_time = True

    intro(animated=True)

    while True:
        print("=== MAIN MENU ===")

        slow_print("1. Start Run")
        slow_print("2. How to Play")
        slow_print("3. Quit\n")

        choice = input("> ").strip()

        if choice == "1":
            print("\nStarting run...\n")
            time.sleep(0.5)

            run_game()

            input("\nRun finished. Press Enter to return to menu...")
            clear()

            # instant Menu after
            intro(animated=False)
            first_time = False

        elif choice == "2":
            how_to_play()
            input("\nPress Enter to return...")
            clear()

            intro(animated=False)

        elif choice == "3":
            print("\nGoodbye.")
            break

        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main_menu()