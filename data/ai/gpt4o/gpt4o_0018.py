import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Possible checkers for up to 5 players

def create_board(rows, columns):
    """Creates an empty board initialized with spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    # Clear the terminal screen
    os.system('clear')
    
    # Print column headers
    column_headers = '  ' + '   '.join(['A', 'B', 'C', 'D', 'E', 'F', 'G'][:len(board[0])])
    print(column_headers)
    
    # Print rows
    for row in board:
        print('+---' * len(row) + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * len(board[0]) + '+')

def is_valid_input(input_char, board):
    """Checks if the input is a valid column."""
    if input_char.isalpha() and len(input_char) == 1:
        col_idx = ord(input_char.upper()) - ord('A')
        if 0 <= col_idx < len(board[0]):
            return True
    return False

def is_column_full(board, col_idx):
    """Checks if a column is full."""
    return board[0][col_idx] != ' '

def drop_checker(board, col_idx, checker):
    """Places a checker in the lowest available space in the column."""
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = checker
            break

def check_winner(board, checker):
    """Checks horizontal, vertical, and diagonal for a win."""
    # Horizontal Check
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == row[col+1] == row[col+2] == row[col+3] == checker:
                return True

    # Vertical Check
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == checker:
                return True

    # Diagonal Check (\ direction)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True

    # Diagonal Check (/ direction)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == checker:
                return True

    return False

def is_draw(board):
    """Checks if the board is completely full."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        user_input = input().strip()

        if not is_valid_input(user_input, board):
            print("Invalid input. Please enter a valid column letter.")
            continue

        col_idx = ord(user_input.upper()) - ord('A')

        if is_column_full(board, col_idx):
            print("Column full. Turn lost.")
            current_player = (current_player + 1) % PLAYERS
            continue

        drop_checker(board, col_idx, CHECKERS[current_player])
        print_board(board)

        if check_winner(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == '__main__':
    main()
