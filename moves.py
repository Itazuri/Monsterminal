from move import Move

MOVES = {
    # Damage Moves
    "fire_bite":    Move("Fire Bite",    8,     effect=None),
    "tackle":       Move("Tackle",       7,     effect=None),
    "water_splash": Move("Water Splash", 7,     effect=None),
    "wave_crash":   Move("Wave Crash",   9,     effect=None),
    "fire_storm":   Move("Fire Storm",   11,    effect=None),
    # Buff/Debuff Moves
    "armor_break":  Move("Armor Break",  0, effect="defense_down"),
    "harden":       Move("Harden",       0, effect="defense_up"),
    "sharpen":      Move("Sharpen",      0, effect="attack_up"),
}