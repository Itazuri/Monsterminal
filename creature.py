class Creature:
    def __init__(self, name, hp, attack, defense, moves):
        self.name = name
        self.level = 1
        self.xp = 0
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.moves = moves

        # maximum of +6 or -6
        self.defense_stage = 0
        self.attack_stage = 0

    def is_alive(self):
        return self.hp > 0

    def reset_combat_stats(self):
        self.defense_stage = 0
        self.attack_stage = 0

    def gain_xp(self, amount):
        self.xp += amount

        while self.xp >= self.xp_to_level():
            self.xp -= self.xp_to_level()
            self.level_up()


    def xp_to_level(self):
        return self.level * 10


    def level_up(self):
        self.level += 1
        self.max_hp += 5
        self.attack += 1
        self.hp = self.max_hp  # heal on level up (might be too op)

        print(f"\n{self.name} leveled up to {self.level}!")