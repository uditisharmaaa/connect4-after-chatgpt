import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # up to 5 players

# Validate constants in case of future extension
assert 2 <= PLAYERS <= 5, "Number of players must be between 2 and 5"
assert COLUMNS <= MAX_COLUMNS, "Number of columns must be 26 or less"

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column labels A, B, C, ...
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(cols)))
    # print horizontal separators and rows
    for r in range(rows):
        print('+' + '---+' * cols)
        print('|' + '|'.join(f" {board[r][c]} " for c in range(cols)) + '|')
    print('+' + '---+' * cols)

def column_letter_to_index(letter):
    return ord(letter) - ord('A')

def is_valid_input(s, columns):
    if len(s) != 1:
        return False
    letter = s[0]
    if not ('A' <= letter <= chr(ord('A') + columns - 1)):
        return False
    return True

def is_column_full(board, col):
    # If the topmost row in this column is not empty, column is full
    return board[0][col] != ' '

def place_checker(board, col, checker):
    # Place checker in lowest available spot in column col
    rows = len(board)
    for r in range(rows-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r, col
    return None  # column is full

def check_four_in_a_row(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

    # Check diagonal down-right (\)
    for r in range(rows-3):
        for c in range(cols-3):
            if (board[r][c] == checker and
                board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and
                board[r+3][c+3] == checker):
                return True

    # Check diagonal up-right (/)
    for r in range(3, rows):
        for c in range(cols-3):
            if (board[r][c] == checker and
                board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and
                board[r-3][c+3] == checker):
                return True

    return False

def is_board_full(board):
    # If no empty cells anywhere, board is full
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    # Initialize board
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]

    # Random first player
    current_index = random.randint(0, PLAYERS-1)

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_index]
        print(f"Player {current_player}, please enter a column:")
        
        # Input loop
        while True:
            choice = input().strip().upper()
            if not is_valid_input(choice, COLUMNS):
                print("Invalid input. Please enter a valid column letter (A-G):")
                continue
            col = column_letter_to_index(choice)
            if is_column_full(board, col):
                # Column full -> lose turn
                # According to assignment: turn is lost if full
                # We notify player and move on
                print("Column is full. Turn lost.")
                input("Press Enter to continue...")
                break  # lose turn
            else:
                # Place checker and break input loop
                place_checker(board, col, current_player)
                break

        # If player placed checker, check for win and draw
        # If column was full and lose turn, no checker placed, so skip

        # Check if last turn placed a checker
        if not is_column_full(board, col) or board[0][col] == current_player:
            # Check win
            if check_four_in_a_row(board, current_player):
                clear_screen()
                print_board(board)
                print(f"Player {current_player} won!")
                return
            # Check draw
            if is_board_full(board):
                clear_screen()
                print_board(board)
                print("The game is a draw!")
                return

        # Next player's turn
        current_index = (current_index + 1) % PLAYERS

if __name__ == '__main__':
    main()
