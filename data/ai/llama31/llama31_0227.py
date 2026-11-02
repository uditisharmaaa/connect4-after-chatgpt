import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with the given dimensions."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print("  A B C D E F G")
    for row in board:
        print("+---" * NUM_COLS + "+")
        print("|", end="")
        for cell in row:
            print(" {} |".format(cell), end="")
        print()
    print("+---" * NUM_COLS + "+")

def get_player_checker(player):
    """Get the checker for the given player."""
    return CHECKERS[player - 1]

def get_player_input(player, board):
    """Get a valid column input from the player."""
    while True:
        column = input("Player {}, please enter a column: ".format(player))
        if len(column)!= 1 or not column.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        column = ord(column.upper()) - ord('A')
        if column < 0 or column >= NUM_COLS:
            print("Column out of range. Please try again.")
            continue
        if board[0][column]!= " ":
            print("Column is full. Please try again.")
            continue
        return column

def place_checker(board, player, column):
    """Place the player's checker in the given column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = get_player_checker(player)
            break

def check_win(board):
    """Check if there is a winner."""
    # Check horizontal wins
    for row in board:
        for i in range(NUM_COLS - 3):
            if row[i]!= " " and row[i] == row[i+1] == row[i+2] == row[i+3]:
                return True
    # Check vertical wins
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if board[i][col]!= " " and board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col]:
                return True
    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col]!= " " and board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                return True
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col]!= " " and board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= " " for row in board for cell in row)

def game():
    """Play the game."""
    board = create_board()
    current_player = random.randint(1, NUM_PLAYERS)
    while True:
        os.system('clear')
        print_board(board)
        column = get_player_input(current_player, board)
        place_checker(board, current_player, column)
        if check_win(board):
            os.system('clear')
            print_board(board)
            print("Player {} won!".format(current_player))
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player % NUM_PLAYERS) + 1

game()
