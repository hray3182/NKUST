from Weapon import Weapon
from Skill import Skill
from Spell import Spell
class Character:
    def __init__(self, name: str, health: int, mana: int, basic_damage: int) -> None:
        self.name = name
        self.health = health
        self.mana = mana
        self.basic_damage = basic_damage 
        self.weapon: Weapon = None
        self.Spells = []
        self.Skills = [] 

    def __str__(self) -> str:
        return f"{self.name} has {self.health} health, {self.mana} mana"
    
    def attack(self, target: 'Character'):
        damage = self.get_damage()
        target.take_damage(damage)
        print(f"{self.name} attacks {target.name} for {damage} damage")

    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage: int):
        self.health -= damage
        print(f"{self.name} takes {damage} damage")
        if not self.is_alive():
            print(f"{self.name} is dead")

    def get_damage(self):
        return self.basic_damage + self.weapon.added_damage if self.weapon else self.basic_damage
    
    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def learn_skill(self, skill: Skill):
        self.Skills.append(skill)

    def learn_spell(self, spell: Spell):
        self.Spells.append(spell)

    def use_skill(self, skill: Skill, target: 'Character'):
        if self.mana >= skill.cost:
            self.mana -= skill.cost
            for attr, change in skill.effect.items():
                if hasattr(target, attr):
                    setattr(target, attr, getattr(target, attr) + change)
                    print(f"{self.name} uses {skill.name} on {target.name} to increase {attr} by {change}")
        else:
            print(f"does not have enough mana to use {skill.name}")

    def use_spell(self, spell: Spell, target: 'Character'):
        if self.mana >= spell.cost:
            print(f"{self.name} uses {spell.name} on {target.name}")
            self.mana -= spell.cost
            target.take_damage(spell.damage)
        else:
            print(f"{self.name} does not have enough mana to use {spell.name}")

