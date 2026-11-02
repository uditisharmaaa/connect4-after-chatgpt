import os
import random
import sys

# Constants for the board dimensions and players
ROWS = 6
COLUMNS = 7

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Max 5 players
NUM_PLAYERS = 2  # Must be between 2 and 5 inclusive

# Number of checkers in a row needed to win
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    # Print column labels
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    row_line = "+" + "---+" * len(board[0])
    for row in board:
        print(row_line)
        print("| " + " | ".join(row) + " |")
    print(row_line)

def column_index_from_letter(letter):
    letter = letter.upper()
    if len(letter) != 1:  # single char only
        return None
    idx = ord(letter) - ord('A')
    if 0 <= idx < COLUMNS:
        return idx
    return None

def get_lowest_empty_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None  # Column full

def is_valid_input(user_input, board):
    if not user_input.isalpha() or len(user_input) != 1:
        return False
    col = column_index_from_letter(user_input)
    if col is None:
        return False
    # Check if column is full
    if board[0][col] != " ":
        return False
    return True

def place_checker(board, col, checker):
    row = get_lowest_empty_row(board, col)
    if row is None:
        # Column full, no placement possible
        return False
    board[row][col] = checker
    return True

def check_winner(board, checker):
    # Check horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLUMNS):
            if board[r][c] == checker:
                count += 1
                if count >= WIN_LENGTH:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(COLUMNS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count >= WIN_LENGTH:
                    return True
            else:
                count = 0

    # Check diagonals (bottom-left to top-right direction)
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(COLUMNS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[r + i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    # Check diagonals (top-left to bottom-right direction)
    for r in range(WIN_LENGTH - 1, ROWS):
        for c in range(COLUMNS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[r - i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    return False

def is_draw(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        sys.exit(1)

    board = create_board(ROWS, COLUMNS)

    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)

        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        user_input = input().strip().upper()

        if not is_valid_input(user_input, board):
            # Invalid input, keep asking
            while True:
                print("Invalid input! Please enter a valid column letter (A-" + chr(ord('A') + COLUMNS -1) + "):")
                user_input = input().strip().upper()
                if is_valid_input(user_input, board):
                    break

        col = column_index_from_letter(user_input)

        placed = place_checker(board, col, current_checker)
        if not placed:
            # Column was full, player loses turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        if check_winner(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Move to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
