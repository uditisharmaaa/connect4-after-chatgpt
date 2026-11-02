import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with all elements initialized with whitespaces."""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the board with column labels."""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| " + " | ".join(row) + " |")
    print("+---+---+---+---+---+---+---+")

def is_valid_input(col):
    """Check if the user input is a valid column label."""
    return col.upper() in string.ascii_uppercase[:BOARD_COLS]

def is_valid_move(board, col):
    """Check if the move is valid (not out of board and not a full column)."""
    return col < BOARD_COLS and board[0][col] == " "

def get_lowest_available_row(board, col):
    """Get the lowest available row in the column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row

def place_checker(board, checker, col):
    """Place the checker at the correct location."""
    row = get_lowest_available_row(board, col)
    board[row][col] = checker

def check_win(board, checker):
    """Check for a win (horizontally, vertically, diagonally)."""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == checker:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == checker:
                return True

    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all([cell!= " " for row in board for cell in row])

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-{string.ascii_uppercase[BOARD_COLS-1]}):")
        col = input().upper()
        if not is_valid_input(col) or not is_valid_move(board, string.ascii_uppercase.index(col)):
            print("Invalid input. Please try again.")
            continue
        place_checker(board, current_player, string.ascii_uppercase.index(col))
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
