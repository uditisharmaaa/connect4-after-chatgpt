import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    # Create a board filled with spaces
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print board with grid lines
    for row in range(ROWS):
        print("+" + "---+" * COLUMNS)
        line = "|"
        for col in range(COLUMNS):
            line += " " + board[row][col] + " |"
        print(line)
    print("+" + "---+" * COLUMNS)

def get_valid_input(current_player):
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        if col_input not in COLUMN_LABELS:
            print("Invalid column. Please enter a letter from A to G.")
            continue
        return col_input

def place_checker(board, col, checker):
    col_index = COLUMN_LABELS.index(col)
    # Place checker in the lowest empty row in the column
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    # Column is full
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (down-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def board_full(board):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players_checkers[current_player_index]
        col_input = get_valid_input(current_checker)
        placed = place_checker(board, col_input, current_checker)
        if not placed:
            # Column full, player loses turn
            print("That column is full. You lose your turn.")
        else:
            print_board(board)
            if check_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if board_full(board):
                print("The game is a draw!")
                break

        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
