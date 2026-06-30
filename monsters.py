import random
from creature import Creature
from moves import MOVES

# Template format: (name, hp, atk, def, spd, move_pool)
NORMAL_ENEMIES = [
    ("FlamingFox", 65, 7, 5, 9, [
        (1,  "tackle"),
        (2,  "fire_bite"),
        (10, "fire_storm"),
    ]),
    ("TankyFish", 75, 5, 8, 4, [
        (1,  "water_splash"),
        (3,  "wave_crash"),
        (4,  "harden"),
    ]),
    ("Rocky", 100, 4, 8, 2, [
        (1,  "harden"),
    ]),
    ("Nany", 30, 14, 3, 12, [
        (1,  "water_splash"),
        (2,  "fire_bite"),
    ]),
]

ELITE_ENEMIES = [
    ("Infernum", 90, 10, 6, 9, [
        (1,  "fire_bite"),
        (2,  "tackle"),
        (4,  "wave_crash"),
        (5,  "armor_break"),
        (14, "fire_storm"),
    ]),
    ("SteelCrab", 95, 6, 12, 3, [
        (1,  "harden"),
        (2,  "tackle"),
        (5,  "armor_break"),
    ]),
    ("DarkShadow", 80, 11, 5, 11, [
        (1,  "fire_bite"),
        (3,  "armor_break"),
        (5,  "sharpen"),
    ]),
    ("Leviathan", 100, 9, 7, 5, [
        (1,  "water_splash"),
        (2,  "wave_crash"),
        (4,  "harden"),
    ]),
]

# Obtainable from the Event
FINDABLE_MONSTERS = [
    ("FlamingFox", 65, 7, 5, 9, [
        (1,  "tackle"),
        (2,  "fire_bite"),
        (10, "fire_storm"),
    ]),
    ("TankyFish", 75, 5, 8, 4, [
        (1,  "water_splash"),
        (3,  "wave_crash"),
        (4,  "harden"),
    ]),
    ("Rocky", 100, 4, 8, 2, [
        (1,  "harden"),
    ]),
    ("Nany", 30, 14, 3, 12, [
        (1,  "water_splash"),
        (2,  "fire_bite"),
    ]),
    ("DarkShadow", 80, 11, 5, 11, [
        (1,  "fire_bite"),
        (3,  "armor_break"),
        (5,  "sharpen"),
    ]),
]


def make_creature(template):
    name, hp, atk, def_, spd, pool = template
    return Creature(
        name, hp=hp, attack=atk, defense=def_, speed=spd,
        move_pool=[(lvl, MOVES[key]) for lvl, key in pool]
    )


def enemy_level(act, offset_min, offset_max):
    base = (act - 1) * 4
    return random.randint(base + offset_min, base + offset_max)


def make_normal_enemy(act=1):
    enemy = make_creature(random.choice(NORMAL_ENEMIES))
    lvl = enemy_level(act, offset_min=1, offset_max=3)
    if lvl > 1:
        enemy.set_level(lvl)
    return enemy


def make_elite_enemy(act=1):
    enemy = make_creature(random.choice(ELITE_ENEMIES))
    lvl = enemy_level(act, offset_min=3, offset_max=5)
    if lvl > 1:
        enemy.set_level(lvl)
    return enemy


def make_random_findable_monster():
    return make_creature(random.choice(FINDABLE_MONSTERS))
