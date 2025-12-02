import json
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich import print


class RoomObject:
    def __init__(self, title, description, enemies=list(), exits=list()):
        self.title = title
        self.description = description
        self.enemies = enemies
        self.exits = exits

    def print_room(self):
        s_width = 60
        print(f"[bold red]{self.title.center(s_width, "-")}[/bold red]")
        print(f"| {self.description.ljust(s_width - 4)} |")
        print("|" + "-"*(s_width-2) + "|")
        #console.print(f"| You See: {you_see.ljust(s_width-13)} |")
        for enemy in self.enemies:
            print(f" - {enemy}")
        print("|" + "-"*(s_width-2) + "|")
        print("|" + "-"*(s_width-2) + "|")
        #console.print(f"| You See: {you_see.ljust(s_width-13)} |")
        for exit in self.exits:
            print(f" - {exit}")
        print("|" + "-"*(s_width-2) + "|")
        print("| " + "What do you do?".ljust(s_width - 4)  + " |")
        #console.print(f"| {option1.ljust(s_width-4)} |")
        #print(f"| {"1. Attack".ljust(s_width-4)} |")
        print(f"| {"q. Quit".ljust(s_width-4)} |")
        print(f"| {"a. Attack".ljust(s_width-4)} |")
        print(f"| {"g. Go To Exit".ljust(s_width-4)} |")
        #console.print(f"| {option2.ljust(s_width-4)} |")
        #console.print(f"| {option3.ljust(s_width-4)} |")
        print("|" + "-"*(s_width-2) + "|")
        #console.print(f"| Log: {log.ljust(s_width-9)} |")
        print("|" + "-"*(s_width-2) + "|")

        choice = Prompt.ask(f"[magenta]What Action?[/magenta]")
        
        return choice
    
    def __str__(self):
        return f"Room: {self.title}"

def LoadAllRooms(file_path="rooms.json"):
    rooms = dict()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            room_list = json.load(f)
        
        for room in room_list:
            title = room["title"]
            description = room["description"]
            enemies = room["enemies"]
            exits = room["exits"]
            r = RoomObject(title, description, enemies, exits)
            #r.load_from_json(title)
            #rooms.append(r)
            rooms[title] = r
            
        return rooms
    except Exception as e:
        print(f"[!] Failed to load JSON: {e}")
        return False


if __name__ == "__main__":
    room_list = LoadAllRooms()
    print(f"{room_list}")

    entry = room_list["Entryway"]
    print(f"{entry}")
    
    #entryway = RoomObject("Entryway", "You see big doors")
    #print(f"{entryway}")
