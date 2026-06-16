import random

RELIC_POOL = [
    {
        "id": "sharp_claws",
        "name": "Sharp Claws",
        "description": "+2 permanent Attack",
        "on_acquire": lambda player: setattr(player, "attack", player.attack + 2),
    },
    {
        "id": "iron_shell",
        "name": "Iron Shell",
        "description": "Start every battle at +1 Defense stage",
        "on_battle_start": lambda player, enemy: setattr(
            player, "defense_stage", min(6, player.defense_stage + 1)
        ),
    },
    {
        "id": "berserker_charm",
        "name": "Berserker Charm",
        "description": "Deal 50% more damage when below 50% HP",
        "on_damage_dealt": lambda player, enemy, move, dmg: (
            int(dmg * 1.5) if player.hp < player.max_hp * 0.5 else dmg
        ),
    },
    {
        "id": "toxic_fang",
        "name": "Toxic Fang",
        "description": "30% chance to poison enemies (−3 HP/turn)",
        # Poison state stored on the enemy as enemy.poisoned = True
        "on_battle_start": lambda player, enemy: setattr(enemy, "poisoned", False),
        "on_damage_dealt": lambda player, enemy, move, dmg: _maybe_poison(enemy, dmg),
        "on_turn_end": lambda player, enemy: _apply_poison(enemy),
    },
    {
        "id": "war_drum",
        "name": "War Drum",
        "description": "Start every battle at +1 Attack stage",
        "on_battle_start": lambda player, enemy: setattr(
            player, "attack_stage", min(6, player.attack_stage + 1)
        ),
    },
    {
        "id": "amulet_of_vigor",
        "name": "Amulet of Vigor",
        "description": "+15 Max HP",
        "on_acquire": lambda player: (
            setattr(player, "max_hp", player.max_hp + 15),
            setattr(player, "hp", player.hp + 15),
        ),
    },
    {
        "id": "vampiric_fang",
        "name": "Vampiric Fang",
        "description": "Heal 2 HP for every hit you land",
        "on_damage_dealt": lambda player, enemy, move, dmg: _lifesteal(player, dmg),
    },
]

# Index for quick lookup
_RELIC_BY_ID = {r["id"]: r for r in RELIC_POOL}


# relic side effect

def _maybe_poison(enemy, dmg):
    if not getattr(enemy, "poisoned", False) and random.random() < 0.30:
        enemy.poisoned = True
        print(f"\n{enemy.name} was poisoned by Toxic Fang!")
    return dmg


def _apply_poison(enemy):
    if getattr(enemy, "poisoned", False) and enemy.is_alive():
        enemy.hp = max(0, enemy.hp - 3)
        print(f"  {enemy.name} takes 3 poison damage! ({enemy.hp}/{enemy.max_hp} HP)")


def _lifesteal(player, dmg):
    healed = min(2, player.max_hp - player.hp)
    if healed > 0:
        player.hp += healed
        print(f"  {player.name} leeches {healed} HP!")
    return dmg

def get_relic(relic_id):
    return _RELIC_BY_ID.get(relic_id)


def give_relic(player, relic_id):
    relic = get_relic(relic_id)
    if relic is None:
        return

    if relic_id in player.relics:
        print(f"\nYou already own {relic['name']}.")
        return

    player.relics.append(relic_id)
    if "on_acquire" in relic:
        relic["on_acquire"](player)
    print(f"\nRelic acquired: {relic['name']} - {relic['description']}")


def random_relic_id(player, exclude_owned=True):
    pool = [r["id"] for r in RELIC_POOL
            if not (exclude_owned and r["id"] in player.relics)]
    return random.choice(pool) if pool else None


def trigger_hook(player, enemy, hook_name, **kwargs):
    damage = kwargs.get("damage")
    move = kwargs.get("move")

    for relic_id in player.relics:
        relic = get_relic(relic_id)
        if relic and hook_name in relic:
            fn = relic[hook_name]
            if hook_name == "on_damage_dealt":
                result = fn(player, enemy, move, damage)
                if result is not None:
                    damage = result
            else:
                fn(player, enemy)

    return damage # Only meaningful for on_damage_dealt


def display_relics(player):
    if not player.relics:
        return
    print("\n  Relics:", end="")
    for relic_id in player.relics:
        r = get_relic(relic_id)
        if r:
            print(f"  [{r['name']}]", end="")
    print()