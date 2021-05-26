from random import randint

# Constants
# Emoji's are for visual purposes (making a terminal game look better?)
WATER = "🌊"
TRACKER_WATER = "🟦"
SHIP_PART = "🟧"
HIT = "❌"
MISS = "⚪"
SIZE = 10  # > 26 will cause problems with coordinates, spacing optimized for 10
SHIPS_LENGTH = [5, 4, 3, 3, 2] # > 5 will require extension of ORDINALS
ORDINALS = ["first", "second", "third", "fourth", "fifth"]
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = [num for num in range(1, 27)]

class BattleshipBoard():
    def __init__(self, tracker=False, rows=SIZE, columns=SIZE):
        self.tracker = tracker
        self.rows = rows
        self.columns = columns
        self.board = []
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
        # Method to print the board as SIZE strings
        for row in self.board:
            print(*row, sep = " ")

    def place_ship(self, length, orientation, row, column):
        # Method to place a ship on the board vertically (orientation == 1) or horizontally (== 0)
        for i in range(length):
            if orientation == 0:
                self.board[row][column + i] = SHIP_PART
            elif orientation == 1:
                self.board[row + i][column] = SHIP_PART


def fire_missile(shooter_tracker, receiving_board, row, column):
    # Shoots a missile at specified coordinate on opponent's board and tracks the hit or miss on player's tracker
        if receiving_board[row][column] == SHIP_PART:
            shooter_tracker[row][column] = HIT
        else:
            shooter_tracker[row][column] = MISS


def has_lost(board):
    # Checks if any SHIP_PART remains, if none remain every ship has been sunk and this board has lost
        for i in range(SIZE):
            if SHIP_PART in board[i]:
                return False
        return True

# This is the board where a player places their ships    
player_board = BattleshipBoard()
computer_board = BattleshipBoard()

# This is the board where a player track hits or misses after firing missiles at their opponent's board
player_tracker = BattleshipBoard(True)
computer_tracker = BattleshipBoard(True)

def game_setup():
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
    print(f"""
Greetings, Captain {name}.
Our forces in the Pacific request back-up.
We have a fleet ready at your disposal.
    """)
    for i in range(len(SHIPS_LENGTH)):
        ship_length = SHIPS_LENGTH[i]
        # Prompt string for vertical or horizontal orientation
        prompt_ship_orientation = f"""Shall we align the next ship along the North-South axis (vertically) or the East-West axis (horizontally)? (Length = {ship_length})
(Type \"v\" for vertical or \"h\" for horizontal) """
        # Prompt string for row
        prompt_ship_row = f"To which latitude shall we send our {ORDINALS[i]} ship? (Length = {ship_length}) (Type letter of row) "
        # Prompt string for column
        prompt_ship_column = f"To which longitude shall we send our {ORDINALS[i]} ship? (Length = {ship_length}) (Type number of column) "

        # Prompt for orientation
        ship_orientation = ""
        while ship_orientation not in ["h", "v"]:
            # Case-insensitive
            ship_orientation = input(prompt_ship_orientation).lower()
        
        # Set ship_orientation to corresponding int and prompt for coordinates, rejecting invalid inputs (ship must fit in grid)
        ship_row = 0
        ship_column = 0
        if ship_orientation == "v":
            ship_orientation = 1
            while ship_row not in range(1, SIZE - ship_length + 2):
                # Case-insensitive, converted to int via index in ALPHABET + 1
                try:
                    ship_row = ALPHABET.index(input(prompt_ship_row).upper()) + 1
                # Prevent non-letter input
                except ValueError:
                    pass
            while ship_column not in range(1, SIZE + 1):
                try:
                    # Converted to int
                    ship_column = int(input(prompt_ship_column))
                # Prevent non-int input
                except ValueError:
                    pass

        elif ship_orientation == "h":
            ship_orientation = 0
            while ship_row not in range(1, SIZE + 1):
                try:
                    ship_row = ALPHABET.index(input(prompt_ship_row).upper()) + 1
                except ValueError:
                    pass
            while ship_column not in range(1, SIZE - ship_length + 2):
                try:
                    ship_column = int(input(prompt_ship_column))
                except ValueError:
                    pass
        
        player_board.place_ship(SHIPS_LENGTH[i], ship_orientation, ship_row, ship_column)
        player_board.print_board()


game_setup()

"""
TO-DO
- prevent ships being placed on other ships
"""