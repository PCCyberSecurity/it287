import json
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich import print


class RoomObject:
    def __init__(self, title, description, enemies=list()):
        self.title = title
        self.description = description
        self.enemies = enemies

    def print_room(self):
        s_width = 60
        print(f"[bold red]{self.title.center(s_width, "-")}[/bold red]")
        print(f"| {self.description.ljust(s_width - 4)} |")
        print("|" + "-"*(s_width-2) + "|")
        #console.print(f"| You See: {you_see.ljust(s_width-13)} |")
        for enemy in self.enemies:
            print(f" - {enemy.name}")
        print("|" + "-"*(s_width-2) + "|")
        print("| " + "What do you do?".ljust(s_width - 4)  + " |")
        #console.print(f"| {option1.ljust(s_width-4)} |")
        print(f"| {"1. Attack".ljust(s_width-4)} |")
        #console.print(f"| {option2.ljust(s_width-4)} |")
        #console.print(f"| {option3.ljust(s_width-4)} |")
        print("|" + "-"*(s_width-2) + "|")
        #console.print(f"| Log: {log.ljust(s_width-9)} |")
        print("|" + "-"*(s_width-2) + "|")

        choice = Prompt.ask(f"[magenta]What Action?[/magenta]")
        
        return choice
    
    def __str__(self):
        return f"Room: {self.title}"
    
if __name__ == "__main__":
    entryway = RoomObject("Entryway", "You see big doors")
    print(f"{entryway}")
