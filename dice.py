import random

def roll_dice(sides=6, count=1):
    rolls = list()
    total = 0
    for i in range(count):
        roll = random.randint(1, sides)
        total += roll
        rolls.append(roll)
    
    return rolls, total

def roll3d6stat():
    rolls, total = roll3d6()
    if total < 8:
        total = 8
    return total

def roll3d6():
    return roll_dice(sides=6, count=3)

def roll2d10():
    return roll_dice(sides=10, count=2)

def rolld6(count=1):
    return roll_dice(sides=6, count=count)

def rolld4(count=1):
    return roll_dice(sides=4, count=count)


if __name__ == "__main__":
    # This was run directly
    print("Testing...")
    rolls, total = roll_dice(sides=6, count=4)
    print(f"Total: {total}\nRolls: {rolls}")

    rolls, total = roll3d6()
    print(f"3d6 Total: {total}\nRolls: {rolls}")
