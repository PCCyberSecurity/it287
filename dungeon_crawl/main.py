import random
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

# Set up Rich console
console = Console()


class PlayerCharacter:
    def __init__(self, name):
        # Store passed in values in the object
        self.name = name
        self.current_hp = 0
        self.str = 8
        self.con = 8
        self.ag = 8
        self.armor = 2
        self.roll_stats()
    
    def __str__(self):
        return f"{self.name}, HP: {self.current_hp}/{self.get_max_hp()}, STR: {self.str}, CON: {self.con}, AG: {self.ag}"

    def roll_stats(self):
        self.str = random.randint(8, 18)
        self.con = random.randint(8, 18)
        self.ag = random.randint(8, 18)
        self.current_hp = self.get_max_hp()
    
    def get_max_hp(self):
        return self.con * 2
    
    def get_damage_max(self):
        return int(self.str / 2)

    def take_damage(self, enemy):
        # Someone hit us - we use their damage max to roll.
        damage = random.randint(1, enemy.get_damage_max())
        total_damage = damage - self.armor
        if total_damage < 0:
            total_damage = 0
        self.current_hp = self.current_hp - total_damage
        print(f"{self.name} took {damage} damage - armor absorbed {self.armor} hps")
    def heal(self):
        heal = random.randint(1, 5)
        self.current_hp = self.current_hp + heal
        print(f"{self.name} healed for {heal} hit points.")
    def revive(self):
        if self.is_dead():
            self.current_hp = self.get_max_hp()
            print(f"{self.name} has been revived with {self.current_hp} hit points.")
    def is_knocked_out(self):
        if self.current_hp < 1:
            return True
        return False
    def is_dead(self):
        if self.current_hp < -10:
            return True
        return False
    
class RoomObject:
    def __init__(self, title, description, enemies=list()):
        self.title = title
        self.description = description
        self.enemies = enemies
    
    def print_room(self):
        s_width = 60
        console.print(f"[bold red]{self.title.center(s_width, "-")}[/bold red]")
        console.print(f"| {self.description.ljust(s_width - 4)} |")
        console.print("|" + "-"*(s_width-2) + "|")
        #console.print(f"| You See: {you_see.ljust(s_width-13)} |")
        for enemy in self.enemies:
            console.print(f" - {enemy.name}")
        console.print("|" + "-"*(s_width-2) + "|")
        console.print("| " + "What do you do?".ljust(s_width - 4)  + " |")
        #console.print(f"| {option1.ljust(s_width-4)} |")
        console.print(f"| {"1. Attack".ljust(s_width-4)} |")
        #console.print(f"| {option2.ljust(s_width-4)} |")
        #console.print(f"| {option3.ljust(s_width-4)} |")
        console.print("|" + "-"*(s_width-2) + "|")
        #console.print(f"| Log: {log.ljust(s_width-9)} |")
        console.print("|" + "-"*(s_width-2) + "|")

        choice = Prompt.ask(f"[magenta]What Action?[/magenta]")
        
        return choice


    



wizard = PlayerCharacter("Harry")

ogre = PlayerCharacter("Ogre")
troll = PlayerCharacter("Troll")

wizard.take_damage(ogre)

print(wizard)
print(ogre)
enemies = []
enemies.append(ogre)
enemies.append(troll)

entryway = RoomObject("Entryway", "You see big doors", enemies)

while wizard.is_knocked_out() is False:
    c = entryway.print_room()

    if (c == '1'):
        # Attack
        enemy = random.choice(enemies)
        enemy.take_damage(wizard)
        wizard.take_damage(enemy)
        print(wizard)
        print(enemy)
        if enemy.is_knocked_out():
            enemies.remove(enemy)
