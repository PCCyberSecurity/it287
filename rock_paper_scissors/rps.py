import os
import random
import re
import sys

from colorama import Fore, Style, init

init()

WIDTH = 60
TOP = 3

player_score = 0
computer_score = 0
round_number = 1
result = ""

# Define function here
def clear_screen():
    print("\x1b[2J\x1b[H", end="", flush=True)

def move_cursor(col, row):
    print(f"\x1b[{row};{col}H", end="", flush=True)

def draw_ui():
    move_cursor(0, TOP)
    # Print top border
    print("╔" + "=" * (WIDTH - 2) + "╗")
    print("║" + "ROCK PAPER SCISSORS".center(WIDTH-2) + "║")
    print("║" + " ".center(WIDTH-2) + "║")
    print("║" + f"Round: {round_number}".ljust(WIDTH-2) + "║")
    print("║" + f"Player Score: {player_score}".ljust(WIDTH-2) + "║")
    print("║" + f"Computer Score: {computer_score}".ljust(WIDTH-2) + "║")
    print("║" + " ".center(WIDTH-2) + "║")
    print("║" + f"    Result: {result}".ljust(WIDTH-2) + "║")
    print("║" + " ".center(WIDTH-2) + "║")
    print("║" + "[R]ock  [P]aper  [S]cissors [Q]uit".center(WIDTH-2) + "║")
    print("║" + " ".center(WIDTH-2) + "║")
    print("║" + "--> ".ljust(WIDTH-2) + "║")
    # Print bottom border
    print("╚" + "=" * (WIDTH - 2) + "╝")

    # Put the cursor at the input line
    move_cursor(6, TOP + 11)
    # print("A", end="", flush=True)
    

def main():
    global player_score, computer_score, round_number, result

    computer_choices = ["r", "p", "s"]
    
    while True:

        player_choice = ""

        clear_screen()

        draw_ui()

        #print("MAIN!")
        response = input()
        response = response.lower()
        if response == "q":
            print("Quitting the game...")
            #sys.exit(0)
            break
        elif response == "r":
            # Handle rock choice
            #print("Player chose Rock")
            result = "Player: Rock"
            player_choice = "r"
        elif response == "p":
            # Handle paper choice
            #print("Player chose Paper")
            result = "Player: Paper"
            player_choice = "p"
        elif response == "s":
            # Handle scissors choice
            #print("Player chose Scissors")
            result = "Player: Scissors"
            player_choice = "s"
        else:
            #print("Invalid input. Please try again.")
            result = "Invalid input. Please try again."

        if not player_choice == "":
            # Computer needs a turn.
            computer_choice = random.choice(computer_choices)
            if (player_choice == "r" and computer_choice == "s"):
                result = Fore.GREEN +"Player wins!" + Fore.RESET + " Rock beats Scissors"
                player_score += 1
            elif (player_choice == "r" and computer_choice == "p"):
                result = Fore.RED +"Computer wins!" + Fore.RESET + " Paper beats Rock" 
                computer_score += 1
            elif (player_choice == "p" and computer_choice == "r"):
                result = "Player wins! Paper beats Rock"
                player_score += 1
            elif (player_choice == "p" and computer_choice == "s"):
                result = "Computer wins! Scissors beats Paper"
                computer_score += 1
            elif (player_choice == "s" and computer_choice == "p"):
                result = "Player wins! Scissors beats Paper"
                player_score += 1
            elif (player_choice == "s" and computer_choice == "r"):
                result = "Computer wins! Rock beats Scissors"
                computer_score += 1
            else:
                result = "It's a tie!"

            #result = result + f" | Computer: {computer_choice.upper()}"

# Main program starts
if __name__ == "__main__":
    # Example usage of the function
    main()


