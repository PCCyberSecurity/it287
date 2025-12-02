from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich import print

from players import PlayerCharacter, LoadAllCharacters
from rooms import RoomObject, LoadAllRooms

from config import p, e

print("[green bold]Welcome To The Game![/]")
p("Game started.")

player_list = LoadAllCharacters()
room_list = LoadAllRooms()

current_player = player_list["Harold"]

print(f"Character List: \n{player_list}")

start_room = "Entryway"

current_room = room_list[start_room]
while True:
    choice = current_room.print_room()

    if choice == "g":
        # Go to a room - which room?
        exits = current_room.exits
        if len(exits) < 1:
            print("No place to go?")
            continue

        exit_index = 0
        for exit in exits:
            print(f"{exit_index}. {exit}")
            exit_index += 1
        c = Prompt.ask(f"[magenta]Which Exit?[/magenta]")
        try:
            c = int(c)
        except:
            c = -1
        if c < len(exits) and c >= 0:
            exit_name = exits[c]
            room_object = room_list[exit_name]
            current_room = room_object
            continue
        else:
            print("Invalid Input!")
            continue


    if choice == "a":
        # Attack - Attack who?
        enemies = current_room.enemies
        if len(enemies) < 1:
            print("No enemies in this room!")
            continue
        
        # There are enemies, print the list.
        enemy_index = 0
        for enemy in enemies:
            print(f"{enemy_index}. {enemy}")
            enemy_index += 1
        c = Prompt.ask(f"[magenta]Which enemy to attack?[/magenta]")
        try:
            c = int(c)
        except:
            c = -1

        if c < len(enemies) and c >= 0:
            enemy_name = enemies[c]
            enemy_object = player_list[enemy_name]
            enemy_object.take_damage(current_player)
            current_player.take_damage(enemy_object)
        else:
            print("Invalid Input!")
            continue
 

    if choice == "q":
        # Quit
        break

print("Game Over!")
#entryway = RoomObject("Entryway", "You see big doors")
#print(f"{entryway}")
