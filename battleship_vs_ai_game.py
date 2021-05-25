from random import randint

# Constants
# Emoji's are for visual purposes (making a terminal game look better?)
WATER = "🌊"
SHIP_PART = "🟧"
HIT = "❌"
MISS = "⚪"
SIZE = 10  # > 26 will cause problems with coordinates, spacing optimized for 10
SHIPS_LENGTH = [2, 3, 3, 4, 5]
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = [num for num in range(1, 27)]

class BattleshipBoard():
    def __init__(self, rows=SIZE, columns=SIZE):
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
                    self.board[row].append(WATER)
    
    def print_board(self):
        # Method to print the board as SIZE strings
        for row in self.board:
            print(*row, sep = " ")

    def place_ship(self, length, orientation, row, column):
        for i in range(length):
            if orientation == 1:
                self.board[row][column + i] = SHIP_PART
            else:
                self.board[row + i][column] = SHIP_PART



class BattleshipTracker(BattleshipBoard):
    def __init__(self, board, rows=SIZE, columns=SIZE):
        self.board = board
        super().__init__(self)


    def receive_missile(self, row, column):
        if self.board[row][column] == SHIP_PART:
            self.board[row][column] = HIT
        else:
            self.board[row][column] = MISS

    def win_game(self):
        for i in range(SIZE):
            if SHIP_PART in self.board[i]:
                return False
        return True

        
player_board = BattleshipBoard()
computer_board = BattleshipBoard()

# Players track the opponent's board based on hits and misses
player_tracker = BattleshipTracker(computer_board)
computer_tracker = BattleshipTracker(player_board)



def game_setup():
    pass

player_board.place_ship(5, 0, 6, 3)
#player_board.fire_missile(7, 3)
#player_board.fire_missile(2, 5)
player_board.print_board()
#print(player_board.lose_game())
print(computer_tracker.board)
print(computer_tracker.win_game())