from move import Move

MOVES = {
    "fire_bite": Move("Fire Bite", 8, "damage"),
    "tackle": Move("Tackle", 7, "damage"),
    "water_splash": Move("Water Splash", 7, "damage"),
    "wave_crash": Move("Wave Crash", 9, "damage"),
    # Buff/Debuff Moves
    "armor_break": Move("Armor Break", "lowers defense", "defense_down"),
    "harden": Move("Harden", "highers_defense", "defense_up"),
    "sharpen": Move("Sharpen", "highers_attack", "attack_up")
}