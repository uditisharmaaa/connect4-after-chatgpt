import os
import random

# Global constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """
    Creates a 2D board with specified rows and columns.
    Initializes all elements with whitespaces.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """
    Prints the current state of the board.
    Labels columns with letters from A to Z.
    """
    os.system('clear')
    print('  ', end='')
    for col in range(cols):
        print(chr(65 + col), end='  ')
    print()
    for row in board:
        print('+---' * cols + '+')
        print('|', end='')
        for cell in row:
            print(' ' + cell + ' |', end='')
        print()
    print('+---' * cols + '+')

def get_player_checker(player):
    """
    Returns the checker symbol for a given player.
    """
    return CHECKERS[player]

def get_column_from_input(input_str, cols):
    """
    Converts user input (column letter) to column index.
    Returns -1 if input is invalid.
    """
    if input_str not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or len(input_str)!= 1:
        return -1
    col_idx = ord(input_str.upper()) - 65
    if col_idx < 0 or col_idx >= cols:
        return -1
    return col_idx

def drop_checker(board, col_idx, checker):
    """
    Places a checker in the specified column.
    Returns False if column is already full.
    """
    for row_idx in range(BOARD_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    """
    Checks if the current player has won.
    Returns True if 4 checkers are in a row horizontally, vertically, or diagonally.
    """
    # Check horizontal wins
    for row in board:
        for col_idx in range(len(row) - 3):
            if row[col_idx] == checker and row[col_idx + 1] == checker and row[col_idx + 2] == checker and row[col_idx + 3] == checker:
                return True

    # Check vertical wins
    for col_idx in range(len(board[0])):
        for row_idx in range(len(board) - 3):
            if board[row_idx][col_idx] == checker and board[row_idx + 1][col_idx] == checker and board[row_idx + 2][col_idx] == checker and board[row_idx + 3][col_idx] == checker:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row_idx in range(len(board) - 3):
        for col_idx in range(len(board[0]) - 3):
            if board[row_idx][col_idx] == checker and board[row_idx + 1][col_idx + 1] == checker and board[row_idx + 2][col_idx + 2] == checker and board[row_idx + 3][col_idx + 3] == checker:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row_idx in range(3, len(board)):
        for col_idx in range(len(board[0]) - 3):
            if board[row_idx][col_idx] == checker and board[row_idx - 1][col_idx + 1] == checker and board[row_idx - 2][col_idx + 2] == checker and board[row_idx - 3][col_idx + 3] == checker:
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full (i.e., it's a draw).
    """
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    # Initialize board and players
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = PLAYERS
    current_player = random.randint(0, players - 1)

    while True:
        print_board(board, BOARD_COLS)
        checker = get_player_checker(current_player)
        print(f"Player {checker}, please enter a column:")
        while True:
            col_input = input().upper()
            col_idx = get_column_from_input(col_input, BOARD_COLS)
            if col_idx!= -1:
                break
            print("Invalid input. Please enter a column letter (A-{}).".format(chr(65 + BOARD_COLS - 1)))

        if drop_checker(board, col_idx, checker):
            if check_win(board, checker):
                print_board(board, BOARD_COLS)
                print(f"Player {checker} won!")
                break
            if check_draw(board):
                print_board(board, BOARD_COLS)
                print("It's a draw!")
                break
            current_player = (current_player + 1) % players
        else:
            print("Column is full. Please choose another column.")

if __name__ == "__main__":
    main()
