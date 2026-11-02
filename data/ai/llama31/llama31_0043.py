import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create a 2D board with whitespaces"""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print("  A", end="")  # print column labels
    for i in range(1, BOARD_COLS):
        print("   " + chr(ord('A') + i), end="")
    print()
    for row in range(BOARD_ROWS):
        print("+---" * BOARD_COLS + "+")
        for col in range(BOARD_COLS):
            print("| " + board[row][col] + " ", end="")
        print("|")
        print("+---" * BOARD_COLS + "+")

def get_player_checker(player_num):
    """Return the checker symbol for the given player"""
    return CHECKERS[player_num - 1]

def is_valid_column(col):
    """Check if the given column is valid (not out of bounds)"""
    return 'A' <= col <= 'G'

def get_column_index(col):
    """Convert column letter to index"""
    return ord(col) - ord('A')

def is_column_full(board, col):
    """Check if the given column is full"""
    return board[0][get_column_index(col)]!= " "

def get_next_open_row(board, col):
    """Get the next open row in the given column"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][get_column_index(col)] == " ":
            return row

def drop_checker(board, row, col, checker):
    """Drop the checker into the given column"""
    board[row][get_column_index(col)] = checker

def check_win(board, checker):
    """Check for a win in any direction"""
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

def check_draw(board):
    """Check for a draw"""
    return all(board[0][col]!= " " for col in range(BOARD_COLS))

def main():
    num_players = 2  # Set the number of players
    if num_players < MIN_PLAYERS or num_players > MAX_PLAYERS:
        raise ValueError("Number of players must be between {} and {}".format(MIN_PLAYERS, MAX_PLAYERS))

    board = create_board(BOARD_ROWS, BOARD_COLS)
    current_player = random.randint(1, num_players)

    print_board(board)

    while True:
        checker = get_player_checker(current_player)
        print("Player {}, please enter a column:".format(checker))

        while True:
            col = input().upper()
            if is_valid_column(col) and not is_column_full(board, col):
                break
            print("Invalid input. Please enter a valid column.")

        row = get_next_open_row(board, col)
        drop_checker(board, row, col, checker)

        print_board(board)

        if check_win(board, checker):
            print("Player {} won!".format(checker))
            break
        elif check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player % num_players) + 1

if __name__ == "__main__":
    main()
