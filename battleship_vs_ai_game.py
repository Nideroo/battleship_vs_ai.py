from random import randint

# Constants
# Emoji's are for visual purposes (making a terminal game look better?)
WATER = "🌊"
TRACKER_WATER = "🟦"
SHIP_PART = "🟧"
HIT = "❌"
MISS = "⚪"
SIZE = 10  # > 26 will cause problems with coordinates, spacing optimized for 10
SHIPS_LENGTH = [2, 3, 3, 4, 5]
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
        for i in range(length):
            if orientation == 0:
                self.board[row][column + i] = SHIP_PART
            else:
                self.board[row + i][column] = SHIP_PART


def fire_missile(shooter_tracker, receiving_board, row, column):
        if receiving_board[row][column] == SHIP_PART:
            shooter_tracker[row][column] = HIT
        else:
            shooter_tracker[row][column] = MISS


def has_won(board):
        for i in range(SIZE):
            if SHIP_PART in board[i]:
                return False
        return True

       
player_board = BattleshipBoard()
computer_board = BattleshipBoard()

# Players track their opponent's board based on hits and misses
player_tracker = BattleshipBoard(True)
computer_tracker = BattleshipBoard(True)

def game_setup():
    print("Welcome to Battleship - the classic naval combat game.")
    name = input("What's your name? ")

    rules_reminder = """
    PLACEHOLDER
    FOR
    RULES REMINDER
    """
    wants_rules_reminder = ""

    while wants_rules_reminder != "y" and wants_rules_reminder != "n":
        wants_rules_reminder = input(f"Would you like a quick refresher on the rules of Battleship, {name}? (y/n) ").lower()
        if wants_rules_reminder == "y":
            print(rules_reminder)
    
    ready_to_start = input("Type anything when you're ready to start the game. ")


game_setup()

# player_board.place_ship(5, 1, 6, 3)
# player_board.fire_missile(7, 3)
# player_board.fire_missile(2, 5)
# print(player_board.board)
# print(computer_tracker.board)
# player_board.print_board()
# computer_tracker.print_board()
