MAX_TEAM_SIZE = 3


class Team:
    def __init__(self, starter):
        self.relics = []
        starter.relics = self.relics
        self.members = [starter]
        self.active_index = 0

    @property
    def active(self):
        return self.members[self.active_index]

    def is_full(self):
        return len(self.members) >= MAX_TEAM_SIZE

    def alive_indices(self):
        return [i for i, m in enumerate(self.members) if m.is_alive()]

    def is_alive(self):
        return len(self.alive_indices()) > 0

    def switch_to(self, index):
        if 0 <= index < len(self.members) and self.members[index].is_alive():
            self.active_index = index
            return True
        return False

    def add_member(self, new_creature):
        if self.is_full():
            return False
        new_creature.relics = self.relics
        self.members.append(new_creature)
        return True

    def replace_member(self, index, new_creature):
        old = self.members[index]
        new_creature.relics = self.relics
        if old.level > 1:
            new_creature.set_level(old.level)
        self.members[index] = new_creature
        return old

    def level_up_all(self):
        for member in self.members:
            member.level_up()

    def reset_combat_stats(self):
        for member in self.members:
            member.reset_combat_stats()
