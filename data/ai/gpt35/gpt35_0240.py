import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_PLAYERS = 2  # Change this to 2-5 for different number of players
WIN_COUNT = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(columns)]
    print("  " + "   ".join(labels))
    # Print board rows
    row_sep = "+" + "---+" * columns
    for row in board:
        print(row_sep)
        print("| " + " | ".join(row) + " |")
    print(row_sep)

def valid_input(user_input, columns):
    if len(user_input) != 1:
        return False
    c = user_input.upper()
    if not ('A' <= c < chr(ord('A') + columns)):
        return False
    return True

def column_index(letter):
    return ord(letter.upper()) - ord('A')

def place_checker(board, col, checker):
    # Places checker in the lowest available row in column col
    # Return True if placed, False if column full
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r + i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal check (down-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal check (up-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def board_full(board):
    # If any empty space found, return False
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    # Validate constants
    if NUM_PLAYERS < MIN_PLAYERS or NUM_PLAYERS > MAX_PLAYERS:
        print(f"Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        return
    if COLUMNS > MAX_COLUMNS:
        print(f"Maximum number of columns is {MAX_COLUMNS}.")
        return

    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {players[current_player_index]}, you start!")

    while True:
        player = players[current_player_index]
        print(f"Player {player}, please enter a column:")
        user_input = input().strip().upper()

        if not valid_input(user_input, COLUMNS):
            # Invalid input, try again without losing turn
            continue

        col = column_index(user_input)

        placed = place_checker(board, col, player)

        if not placed:
            # Column full: player loses turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_winner(board, player):
            print(f"Player {player} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
