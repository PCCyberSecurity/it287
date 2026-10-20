from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
import random

# Set up Rich console
console = Console()

enemy_hp = 10

console.print("[bold yellow]Cast a spell:[/bold yellow]")
console.print("📜 - 1. [green]Expelliarmus[/green]")
console.print("📜 - 2. [green]Alohomora[/green]")
console.print("📜 - 3. [green]Avada Kedavra[/green]")

spell = Prompt.ask("[magenta]Which spell to cast?[/magenta]")

if (spell.lower() in "expelliarmus") or (spell == "1"):
    console.print("🔮 Disarmed your enemy!")
    roll = random.randint(1, 6)
    enemy_hp = enemy_hp - roll
    console.print(f"🎲 Damage dealt: {roll}")
elif(spell.lower() in "alohomora") or (spell == "2"):
    console.print("🚪 Door unlocked.")
elif(spell.lower() in "avada kedavra") or (spell == "3"):
    console.print("💀 You went full dark wizard!")
    enemy_hp = enemy_hp - 10
else:
    console.print("📜 Spell not in the library.")

console.print("📜 The duel is complete!")


import random

random.seed(42)

rolls = [random.randint(1, 6) for _ in range(6)]

print(rolls)