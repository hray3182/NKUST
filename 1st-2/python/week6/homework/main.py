from Character import Character
from Weapon import Weapon
from Skill import Skill
from Spell import Spell

if __name__ == "__main__":
    hero = Character("Hero", 100, 100, 10)
    boss = Character("Boss", 200, 50, 20)

    sword = Weapon("Sword", 10)

    fire_ball = Spell("Fire Ball", 20, 50)
    ice_storm = Spell("Ice Storm", 30, 70)

    health = Skill("Health", 10, {"health": 10})
    war_cry = Skill("War Cry", 20, {"basic_damage": 10})

    hero.equip_weapon(sword)
    hero.learn_spell(fire_ball)
    hero.learn_spell(ice_storm)
    hero.learn_skill(health)
    hero.learn_skill(war_cry)

    print(hero)
    print(boss)
    print("-"*20)

    hero.attack(boss)
    hero.use_spell(fire_ball, boss)
    hero.use_skill(health, hero)
    hero.use_skill(war_cry, hero)
    hero.attack(boss)
    hero.use_spell(ice_storm, boss)

    print("-"*20)
    print(hero)
    print(boss)
    print("-"*20)
    
    hero.attack(boss)