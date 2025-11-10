from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich import print

from players import PlayerCharacter, LoadAllCharacters
from rooms import RoomObject

print("[green bold]Welcome To The Game![/]")

player_list = LoadAllCharacters()

print(f"Character List: \n{player_list}")


entryway = RoomObject("Entryway", "You see big doors")
print(f"{entryway}")
