import random

# Constants
# Emoji's are for visual purposes (making a terminal game look better?)
WATER = "🌊"
TRACKER_WATER = "🟦"
SHIP_PARTS = "🟥🟧🟨🟩🟪"
HIT = "❌"
MISS = "⚪"
SIZE = 10  # > 26 will cause problems with coordinates, spacing optimized for 10
SHIPS_LENGTH = [5, 4, 3, 3, 2] # > 5 will require extension of SHIP_PARTS and ORDINALS
ORDINALS = ["first", "second", "third", "fourth", "fifth"]
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = [num for num in range(1, 27)]

class BattleshipBoard():
    def __init__(self, tracker=False, rows=SIZE, columns=SIZE):
        self.tracker = tracker
        self.rows = rows
        self.columns = columns
        self.board = []
        self.ships_coords = {}
        # Make a grid of (SIZE + 1) x (SIZE + 1), so we can have letters and numbers in respectively the first column and row for a coordinate system
        for row in range(SIZE + 1):
            self.board.append([])
            for column in range(SIZE + 1):
                if row == 0 and column == 0:
                    self.board[row].append(".")
                elif row == 0 and column != 0:
                    self.board[row].append(f" {NUMBERS[column - 1]}")
                elif row != 0 and column == 0:
                    self.board[row].append(f"{ALPHABET[row - 1]}")
                else:
                    if self.tracker == False:
                        self.board[row].append(WATER)
                    else:
                        self.board[row].append(TRACKER_WATER)
    
    def print_board(self):
        # Print the board as SIZE strings
        for row in self.board:
            print(*row, sep = " ")

    def create_ship_coords(self, length, orientation, row, column):
        ship_coords = []
        # If all coords contain WATER, it is a valid set of coords and the ship may be placed there with place_ship
        if orientation == "h":
            for i in range(length):
                try:
                    if self.board[row][column + i] == WATER:
                        ship_coords.append((row, column + i))
                    else:
                        return False
                except IndexError:
                    return False
        elif orientation == "v":
            for i in range(length):
                try:
                    if self.board[row + i][column] == WATER:
                        ship_coords.append((row + i, column))
                    else:
                        return False
                except IndexError:
                    return False
        return ship_coords
    
    def place_ship(self, ship_part, ship_coords):
        # Place the ship on the board
        for coords in ship_coords:
            row, column = coords[0], coords[1]
            self.board[row][column] = ship_part

    def get_shot(self, missile_coords):
        row, column = missile_coords[0], missile_coords[1]
        if self.board[row][column] in SHIP_PARTS:
            self.board[row][column] = HIT
            return True
        elif self.board[row][column] == WATER:
            print("MISS PLACEHOLDER")
            self.board[row][column] = MISS
            return False        

    def has_lost(self):
        for i in range(SIZE + 1):
            for ship_part in SHIP_PARTS:
                if ship_part in self.board[i]:
                    return False
        return True


# This is the board where a player places their ships    
player_board = BattleshipBoard()
computer_board = BattleshipBoard()

# This is the board where a player track hits or misses after firing missiles at their opponent's board
player_tracker = BattleshipBoard(True)
computer_tracker = BattleshipBoard(True)

def player_setup():
    # Gather neccessary info from player and give opportunity to read rules
    print("Welcome to Battleship - the classic naval combat game.")
    name = input("What's your name? ")

    rules_reminder = """
    PLACEHOLDER
    FOR
    RULES REMINDER
    """
    wants_rules_reminder = ""
    # Re-prompts after other input, but will accept case-insensitive y/n
    while wants_rules_reminder != "y" and wants_rules_reminder != "n":
        wants_rules_reminder = input(f"Would you like a quick refresher on the rules of Battleship, Captain {name}? (y/n) ").lower()
        if wants_rules_reminder == "y":
            print(rules_reminder)
    
    # Gives user chance to read rules if they requested them, before we print the board
    ready_to_start = input("Type anything when you're ready to start the game. ")

    player_board.print_board()
    print(f"Greetings, Captain {name}. \nOur forces in the Pacific request back-up. \nWe have a fleet ready at your disposal.")

    for i in range(len(SHIPS_LENGTH)):
        ship_length = SHIPS_LENGTH[i]
        # Message to prompt for orientation (vertical or horizontal)
        prompt_ship_orientation = f"""Shall we align the next ship along the North-South axis (vertically) or the East-West axis (horizontally)? (Length = {ship_length}) \n(Type \"v\" for vertical or \"h\" for horizontal) """
        # Message to prompt for row
        prompt_ship_row = f"To which latitude shall we send our {ORDINALS[i]} ship? (Length = {ship_length}) (Type letter of row) "
        # Message to prompt for column
        prompt_ship_column = f"To which longitude shall we send our {ORDINALS[i]} ship? (Length = {ship_length}) (Type number of column) "

        # Prompt for orientation
        ship_orientation = ""
        while ship_orientation not in ["h", "v"]:
            # Case-insensitive
            ship_orientation = input(prompt_ship_orientation).lower()


def computer_setup():
    pass

#player_setup()
#computer_setup()

def player_turn():
    pass

def computer_turn():
    pass

# Game is played until one person has lost (by having no more ship parts)
while player_board.has_lost == False and computer_board.has_lost == False:
    player_turn()
    computer_turn()

if player_board.has_lost():
    print("LOST PLACEHOLDER")

if computer_board.has_lost():
    print("WON PLACEHOLDER")

print(player_board.create_ship_coords(5, "h", 10, 10))

"""
TO-DO
- type rules reminder
- rework ships as lists of tuples

"""
