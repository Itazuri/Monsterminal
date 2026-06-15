class Creature:
    def __init__(self, name, hp, attack, defense, moves):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.moves = moves

        # combat-only stat stages (pokemon-style, -6 to +6)
        self.defense_stage = 0
        self.attack_stage = 0

    def is_alive(self):
        return self.hp > 0

    def reset_combat_stats(self):
        self.defense_stage = 0
        self.attack_stage = 0