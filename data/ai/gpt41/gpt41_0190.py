import os
import random

# -------- Constants --------
ROWS = 6
COLS = 7
MAX_COLS = 26
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4

# -------- Board Functions --------

def create_board(rows, cols):
    """Creates an empty board with given rows and cols"""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    cols = len(board[0])
    # Print column headers
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    # Print horizontal line
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

# -------- Game Logic Functions --------

def choose_first_player(num_players):
    return random.randint(0, num_players - 1)

def column_full(board, col):
    return board[0][col] != ' '

def valid_column(col_letter, cols):
    if len(col_letter) != 1:
        return False
    letter = col_letter[0]
    if not ('A' <= letter <= chr(ord('A') + cols - 1)):
        return False
    return True

def get_column_index(col_letter):
    return ord(col_letter) - ord('A')

def insert_checker(board, col, checker):
    # Start from bottom row, place checker in first available row.
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False  # If column is full

def is_draw(board):
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Diagonal (\)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[r + i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    # Diagonal (/)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[r - i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    return False

# -------- Main Game Loop --------

def main():
    # Game settings (as per assignment: 6x7, 2 players)
    rows = ROWS
    cols = COLS
    num_players = NUM_PLAYERS
    checkers = CHECKERS[:num_players]

    # Create game board
    board = create_board(rows, cols)

    # Choose first player at random
    current_player = choose_first_player(num_players)

    # Print initial empty board
    print_board(board)

    while True:
        checker = checkers[current_player]
        print("Player {}, please enter a column:".format(checker))

        # Input loop
        while True:
            col_input = input().strip().upper()
            if not valid_column(col_input, cols):
                print("Invalid input. Please enter a column from A to {}:".format(chr(ord('A') + cols - 1)))
                continue

            col = get_column_index(col_input)
            if column_full(board, col):
                print("Column is full. You lose your turn.")
                col = None
                break  # lose turn if column is full (as per assignment)
            break

        if col is not None:
            # Place checker
            insert_checker(board, col, checker)

        print_board(board)

        # Check for win
        if check_win(board, checker):
            print("Player {} won!".format(checker))
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_player = (current_player + 1) % num_players

if __name__ == '__main__':
    main()
