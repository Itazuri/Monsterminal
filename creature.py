MAX_MOVES = 4

# % of base stat gained per level
HP_GROWTH      = 0.12
ATTACK_GROWTH  = 0.08
DEFENSE_GROWTH = 0.08
SPEED_GROWTH   = 0.05


def _scale(base, level, rate, minimum=1):
    return max(minimum, round(base + base * rate * (level - 1)))


class Creature:
    def __init__(self, name, hp, attack, defense, move_pool, speed=5):
        self.name = name
        self.level = 1
        # base stats
        self._base_hp      = hp
        self._base_attack  = attack
        self._base_defense = defense
        self._base_speed   = speed
        # leveled stats
        self.max_hp  = hp
        self.hp      = hp
        self.attack  = attack
        self.defense = defense
        self.speed   = speed

        self.move_pool = sorted(move_pool, key=lambda x: x[0])

        # Start with lvl 1 moves
        self.moves = [move for lvl, move in self.move_pool if lvl == 1][:MAX_MOVES]

        # Learned move tracker
        self._learned = set()
        for lvl, move in self.move_pool:
            if lvl == 1:
                self._learned.add(id(move))

        # Relics — player only
        self.relics = []

        # Combat stages
        self.defense_stage = 0
        self.attack_stage  = 0

    def is_alive(self):
        return self.hp > 0

    def reset_combat_stats(self):
        self.defense_stage = 0
        self.attack_stage  = 0

    def _recalc_stats(self):
        """Recompute all derived stats from base stats + current level.
        Returns the HP headroom gained (new max_hp - old max_hp)."""
        prev_max     = self.max_hp
        self.max_hp  = _scale(self._base_hp,      self.level, HP_GROWTH)
        self.attack  = _scale(self._base_attack,  self.level, ATTACK_GROWTH)
        self.defense = _scale(self._base_defense, self.level, DEFENSE_GROWTH)
        self.speed   = _scale(self._base_speed,   self.level, SPEED_GROWTH)
        return self.max_hp - prev_max

    # heal fraction of hp on level up
    LEVEL_UP_HEAL_FRAC = 0.5

    def level_up(self):
        self.level += 1
        hp_gained = self._recalc_stats()

        healed = max(1, int(hp_gained * self.LEVEL_UP_HEAL_FRAC))
        self.hp = min(self.max_hp, self.hp + healed)

        print(f"\n{self.name} leveled up to level {self.level}!")
        print(f"  ATK {self.attack}  DEF {self.defense}  SPD {self.speed}  "
              f"HP {self.hp}/{self.max_hp}  (+{healed} HP)")

        for lvl, move in self.move_pool:
            if lvl == self.level and id(move) not in self._learned:
                self._learned.add(id(move))
                self._try_learn_move(move)

    def set_level(self, target_level):
        self.level = target_level
        self._recalc_stats()
        self.hp = self.max_hp

        for lvl, move in self.move_pool:
            if lvl <= self.level and id(move) not in self._learned:
                self._learned.add(id(move))
                if len(self.moves) < MAX_MOVES:
                    self.moves.append(move)
                else:
                    self.moves.pop(0)
                    self.moves.append(move)


    def _try_learn_move(self, new_move):
        if len(self.moves) < MAX_MOVES:
            self.moves.append(new_move)
            print(f"{self.name} learned {new_move.name}!")
            return

        print(f"\n{self.name} wants to learn {new_move.name}!")
        print(f"But {self.name} already knows {MAX_MOVES} moves.\n")

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