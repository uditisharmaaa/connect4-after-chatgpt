import os
import random
import string

# Constants (you can change these for testing, but submit with these values)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
TOKENS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
WIN_LENGTH = 4  # Always 4 as per assignment

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Header with letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(letters))
    # Top border
    print("+" + ("---+" * cols))
    # Rows
    for r in range(len(board)):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + ("---+" * cols))

def get_column_input(num_cols):
    valid_letters = [string.ascii_uppercase[i] for i in range(num_cols)]
    while True:
        user_in = input("Please enter a column ({}-{}): ".format(valid_letters[0], valid_letters[-1])).strip().upper()
        if len(user_in) != 1:
            print("Invalid input. Enter a single letter.")
            continue
        if user_in not in valid_letters:
            print("Invalid column. Choose a letter between {} and {}.".format(valid_letters[0], valid_letters[-1]))
            continue
        return valid_letters.index(user_in)

def place_checker(board, col, token):
    # Place from bottom up
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return True
    return False  # Column full

def check_win(board, token):
    rows = len(board)
    cols = len(board[0])
    n = WIN_LENGTH

    # Horizontal
    for r in range(rows):
        for c in range(cols - n + 1):
            ok = True
            for k in range(n):
                if board[r][c + k] != token:
                    ok = False
                    break
            if ok:
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - n + 1):
            ok = True
            for k in range(n):
                if board[r + k][c] != token:
                    ok = False
                    break
            if ok:
                return True

    # Diagonal down-right
    for r in range(rows - n + 1):
        for c in range(cols - n + 1):
            ok = True
            for k in range(n):
                if board[r + k][c + k] != token:
                    ok = False
                    break
            if ok:
                return True

    # Diagonal up-right
    for r in range(n - 1, rows):
        for c in range(cols - n + 1):
            ok = True
            for k in range(n):
                if board[r - k][c + k] != token:
                    ok = False
                    break
            if ok:
                return True

    return False

def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if COLS < 1 or COLS > 26:
        print("COLS must be between 1 and 26.")
        return

    board = create_board(ROWS, COLS)
    # Random starting player
    current_index = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        current_token = TOKENS[current_index]
        print("Player {}, please enter a column:".format(current_token))
        col = get_column_input(COLS)

        placed = place_checker(board, col, current_token)

        clear_screen()
        print_board(board)

        if placed:
            if check_win(board, current_token):
                print("Player {} won!".format(current_token))
                break
            if board_full(board):
                print("It's a draw!")
                break
        else:
            print("Column is full! Player {} loses the turn.".format(current_token))

        # Next player's turn
        current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
