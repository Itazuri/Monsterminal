MAX_MOVES = 4

class Creature:
    def __init__(self, name, hp, attack, defense, move_pool, speed=5):
        self.name = name
        self.level = 1
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed

        self.move_pool = sorted(move_pool, key=lambda x: x[0])

        # Start with lvl 1 moves
        self.moves = [move for lvl, move in self.move_pool if lvl == 1][:MAX_MOVES]

        # Which moves have been learned tracker
        self._learned = set()
        for lvl, move in self.move_pool:
            if lvl == 1:
                self._learned.add(id(move))

        # Relics only for player 
        self.relics = []

        # Combat stages
        self.defense_stage = 0
        self.attack_stage = 0

    def is_alive(self):
        return self.hp > 0

    def reset_combat_stats(self):
        self.defense_stage = 0
        self.attack_stage = 0

    def gain_level(self, amount):
        self.level += amount

    def level_up(self):
        self.level += 1
        self.max_hp += 5
        self.attack += 1
        self.hp = self.max_hp  # heal on level up

        print(f"\n{self.name} leveled up to level {self.level}!")

        # Check for new learnable moves
        for lvl, move in self.move_pool:
            if lvl == self.level and id(move) not in self._learned:
                self._learned.add(id(move))
                self._try_learn_move(move)

    def _try_learn_move(self, new_move):
        if len(self.moves) < MAX_MOVES:
            self.moves.append(new_move)
            print(f"{self.name} learned {new_move.name}!")
            return

        # When at cap ask, to learn or forget
        print(f"\n{self.name} wants to learn {new_move.name}!")
        print(f"But {self.name} already knows {MAX_MOVES} moves.")
        print("Which move should be forgotten? (or 0 to not learn it)\n")

        all_moves = self.moves + [new_move]
        for i, move in enumerate(all_moves, start=1):
            tag = " ← NEW" if move is new_move else ""
            print(f"  {i}. {move.name}{tag}")
        print("  0. Don't learn the new move")

        while True:
            try:
                choice = int(input("> "))
                if choice == 0:
                    print(f"{self.name} did not learn {new_move.name}.")
                    return
                if 1 <= choice <= len(all_moves):
                    forgotten = all_moves[choice - 1]
                    if forgotten is new_move:
                        print(f"{self.name} did not learn {new_move.name}.")
                    else:
                        self.moves[choice - 1] = new_move
                        print(f"{self.name} forgot {forgotten.name} and learned {new_move.name}!")
                    return
                print(f"Pick 0-{len(all_moves)}.")
            except ValueError:
                print("Invalid input.")

    def set_level(self, target_level):
        while self.level < target_level:
            self.level += 1
            self.max_hp += 5
            self.attack += 1
            for lvl, move in self.move_pool:
                if lvl == self.level and id(move) not in self._learned:
                    self._learned.add(id(move))
                    if len(self.moves) < MAX_MOVES:
                        self.moves.append(move)
                    # newest move replaces oldest move
                    else:
                        self.moves.pop(0)
                        self.moves.append(move)
        self.hp = self.max_hp