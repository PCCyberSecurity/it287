import os
import random
import re
import sys

from colorama import Fore, Style, init

init()

WIDTH = 60
TOP = 3

choices = ["rock", "paper", "scissors"]

player_score = 0
computer_score = 0
round_num = 1

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


# ─────────────────────────────────────────────
# Terminal helpers
# ─────────────────────────────────────────────

def visible_length(text):
    return len(ANSI_RE.sub("", text))


def box_line(text=""):
    padding = WIDTH - visible_length(text)
    return f"║{text}{' ' * max(0, padding)}║"


def border(left, right):
    return left + ("═" * WIDTH) + right


def move_cursor(row, col=1):
    print(f"\033[{row};{col}H", end="")


def update_line(row, text):
    move_cursor(TOP + row - 1)
    print(f"\033[2K{text}", end="", flush=True)


def clear_screen():
    print("\033[2J\033[H", end="", flush=True)


# ─────────────────────────────────────────────
# Direct keypress
# ─────────────────────────────────────────────

def get_key():
    if os.name == "nt":
        import msvcrt

        key = msvcrt.getwch()

        if key in ("\x00", "\xe0"):
            msvcrt.getwch()
            return ""

        return key.lower()

    import termios
    import tty

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(
            fd,
            termios.TCSADRAIN,
            old_settings
        )

    return key.lower()


# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────

def draw_ui():
    lines = [
        border("╔", "╗"),                                      # 1
        box_line("                    ROCK PAPER SCISSORS"),      # 2
        box_line(                                               # 3
            f"Round: {round_num:<5}"
            f"       You: {player_score:<5}"
            f"       Computer: {computer_score:<5}"
        ),
        box_line(),                                            # 4
        box_line("                     Result:"),                 # 5
        box_line(),                                            # 6
        box_line(                                               # 7
            "[R] Rock    [P] Paper    [S] Scissors    [Q] Quit"
        ),
        box_line(),                                            # 8
        box_line(">"),                                         # 9
        border("╚", "╝"),                                      # 10
    ]

    for row, line in enumerate(lines, start=1):
        move_cursor(TOP + row - 1)
        print(line, end="")

    sys.stdout.flush()


# ─────────────────────────────────────────────
# Game
# ─────────────────────────────────────────────

def play_round(player):
    global player_score
    global computer_score

    computer = random.choice(choices)

    if player == computer:
        result = "DRAW"
        color = Fore.YELLOW

    elif (
        (player == "rock" and computer == "scissors")
        or
        (player == "paper" and computer == "rock")
        or
        (player == "scissors" and computer == "paper")
    ):
        result = "YOU WIN"
        color = Fore.GREEN
        player_score += 1

    else:
        result = "COMPUTER WINS"
        color = Fore.RED
        computer_score += 1

    update_line(
        3,
        box_line(
            f"Round: {round_num:<5}"
            f"       You: {player_score:<5}"
            f"       Computer: {computer_score:<5}"
        )
    )

    update_line(
        5,
        box_line(
            f"{color}{result:^60}{Style.RESET_ALL}"
        )
    )


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

shortcuts = {
    "r": "rock",
    "p": "paper",
    "s": "scissors",
}

try:
    clear_screen()

    # Move down before drawing the UI.
    move_cursor(TOP)

    # Hide cursor.
    print("\033[?25l", end="", flush=True)

    draw_ui()

    while True:

        # Prompt = UI row 9
        move_cursor(TOP + 8, 4)

        key = get_key()

        if key == "q":
            break

        if key not in shortcuts:
            update_line(
                5,
                box_line(
                    f"{Fore.RED}"
                    f"{'INVALID KEY':^60}"
                    f"{Style.RESET_ALL}"
                )
            )
            continue

        play_round(shortcuts[key])

        round_num += 1

finally:
    print("\033[?25h", end="", flush=True)
    sys.stdout.flush()
