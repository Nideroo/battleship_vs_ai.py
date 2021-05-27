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
        print("")
        # Print the board as SIZE strings
        for row in self.board:
            print(*row, sep = " ")
        print("")

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

    def get_shot(self, shooter, tracker, missile_coords):
        row, column = missile_coords[0], missile_coords[1]
        if self.board[row][column] in SHIP_PARTS:
            if shooter == "player":
                print("player has hit")
            elif shooter == "computer":
                print("computer has hit")

            self.board[row][column] = HIT
            tracker.board[row][column] = HIT
        elif self.board[row][column] == WATER:
            print("MISS PLACEHOLDER")
            tracker.board[row][column] = MISS      

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

    # Ship placement
    # Loop will repeat for every ship that needs to be placed
    for i in range(len(SHIPS_LENGTH)):
        ship_length = SHIPS_LENGTH[i]
        # Message to prompt for orientation (vertical or horizontal)
        prompt_ship_orientation = f"Shall we align the next ship along the North-South axis (vertically) or the East-West axis (horizontally)? (Length = {ship_length}) \n(Type \"v\" for vertical or \"h\" for horizontal) "
        # Message to prompt for coords
        prompt_ship_row_and_column = f"To which latitude and longitude shall we send our {ORDINALS[i]} ship? (Length = {ship_length}) (Type letter of row, number of column) "

        # Prompt for orientation
        ship_orientation = ""
        while ship_orientation not in ["h", "v"]:
            # Case-insensitive
            ship_orientation = input(prompt_ship_orientation).lower()
        
        # Will guarantee first condition check to evaluate to False
        ship_row = SIZE + 2
        ship_column = SIZE + 2

        while player_board.create_ship_coords(ship_length, ship_orientation, ship_row, ship_column) == False:
            try:
                prompted_row_and_column = input(prompt_ship_row_and_column).upper()
                ship_row, ship_column = ALPHABET.index(prompted_row_and_column[0]) + 1, int(prompted_row_and_column[1:])
            except ValueError:
                continue
        
        # Once we have a valid ship_row and ship_column we can actually create the coords and place the ship
        ship_part = SHIP_PARTS[i]
        ship_coords = player_board.create_ship_coords(ship_length, ship_orientation, ship_row, ship_column)
        player_board.place_ship(ship_part, ship_coords)
        player_board.print_board()
    
    print(f"Captain {name}! \nIt seems the enemy forces have detected our presence. \nIt is imperative that we launch our attack first. \nWe trust in your leadership!\n")
        

def computer_setup():
    for i in range(len(SHIPS_LENGTH)):
        ship_length = SHIPS_LENGTH[i]

        possible_orientations = ["h", "v"]
        ship_orientation = possible_orientations[random.randint(0, 1)]

        ship_row = SIZE + 2
        ship_column = SIZE + 2

        while computer_board.create_ship_coords(ship_length, ship_orientation, ship_row, ship_column) == False:
            ship_row, ship_column = random.randint(1, SIZE), random.randint(1, SIZE)

        ship_part = SHIP_PARTS[i]
        ship_coords = computer_board.create_ship_coords(ship_length, ship_orientation, ship_row, ship_column)
        computer_board.place_ship(ship_part, ship_coords)
    

player_setup()
computer_setup()

def create_missile_coords(target, tracker, row, column):
    missile_coords = ()
    try:
        if target.board[row][column] == WATER or target.board[row][column] in SHIP_PARTS:
            if tracker.board[row][column] == HIT or tracker.board[row][column] == MISS:
                return False
            missile_coords = (row, column)
            return missile_coords
        else:
            return False
    except IndexError:
        return False


def player_turn():
    print("This is roughly where the enemy fleet is located:")
    player_tracker.print_board()
    prompt_missile_row_and_column = "Where should we fire a missile at? (Type letter of row, number of column) "

    missile_row = SIZE + 2
    missile_column = SIZE + 2

    while create_missile_coords(computer_board, player_tracker, missile_row, missile_column) == False:
            try:
                prompted_missile_coords = input(prompt_missile_row_and_column).upper()
                missile_row, missile_column = ALPHABET.index(prompted_missile_coords[0]) + 1, int(prompted_missile_coords[1:])
            except ValueError:
                continue

    missile_coords = create_missile_coords(computer_board, player_tracker, missile_row, missile_column)
    computer_board.get_shot("player", player_tracker, missile_coords)
    player_tracker.print_board()
    

def computer_turn():
    missile_row = SIZE + 2
    missile_column = SIZE + 2

    while create_missile_coords(player_board, computer_tracker, missile_row, missile_column) == False:
            missile_row, missile_column = random.randint(1, SIZE), random.randint(1, SIZE)

    missile_coords = create_missile_coords(player_board, computer_tracker, missile_row, missile_column)
    player_board.get_shot("computer", computer_tracker, missile_coords)
    print("This is the current status of our fleet:")
    player_board.print_board()


# Game is played until one person has lost (by having no more ship parts)
while True:
    player_turn()
    computer_turn()
    if player_board.has_lost():
        print("LOST PLACEHOLDER")
        break
    if computer_board.has_lost():
        print("WON PLACEHOLDER")
        break

"""
TO-DO
- replace PLACEHOLDERs
"""
