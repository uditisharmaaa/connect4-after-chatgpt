import os
import random
import string

# Constants
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D list representing the game board."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear')
    print("  " + "   ".join(string.ascii_uppercase[:NUM_COLS]))
    print("+---" * NUM_COLS + "+")
    for row in board:
        print("|   " * NUM_COLS + "|")
        print("+---" * NUM_COLS + "+")
    print("Player {}, please enter a column:".format(get_current_player()))

def get_current_player():
    """Return the current player's checker."""
    return CHECKERS[random.randint(0, len(CHECKERS) - 1)]

def validate_input(col):
    """Check if the user's input is a valid column."""
    return col in string.ascii_uppercase[:NUM_COLS]

def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    col_idx = string.ascii_uppercase.index(col)
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = checker
            break

def check_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal locations for win
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(NUM_COLS - 3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= " " for row in board for cell in row)

def game():
    """Play the Connect 4 game."""
    board = create_board()
    players = CHECKERS[:2]
    current_player_idx = random.randint(0, len(players) - 1)
    while True:
        print_board(board)
        col = input().upper()
        while not validate_input(col):
            print("Invalid input. Please enter a valid column.")
            col = input().upper()
        place_checker(board, col, players[current_player_idx])
        if check_win(board, players[current_player_idx]):
            print_board(board)
            print("Player {} won!".format(players[current_player_idx]))
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player_idx = (current_player_idx + 1) % len(players)

if __name__ == "__main__":
    game()
