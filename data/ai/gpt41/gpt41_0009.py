import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYER_CHARS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Set to 2 for submission as per instructions

# Functions to handle board creation, printing, turns, win checking, etc.

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def clear_screen():
    os.system('clear')

def print_board(board):
    # Print column headers (A, B, C, ...)
    col_headers = "  " + "   ".join(string.ascii_uppercase[:len(board[0])])
    print(col_headers)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(row))

def get_valid_input(board):
    columns = len(board[0])
    valid_letters = string.ascii_uppercase[:columns]
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) == 1 and col_input in valid_letters:
            col_index = ord(col_input) - ord('A')
            # Check if column is not full
            if board[0][col_index] == " ":
                return col_index
            else:
                print("Column is full. You lose your turn.")
                return None  # Lose turn if column is valid but full
        else:
            print("Invalid input. Enter a letter from {} to {} that is not full."
                  .format(valid_letters[0], valid_letters[-1]))

def place_checker(board, col, symbol):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = symbol
            return True
    # Should not happen if we validated before, but a safety
    return False

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == symbol for i in range(4)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r+i][c] == symbol for i in range(4)):
                return True

    # Diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == symbol for i in range(4)):
                return True

    # Diagonal (down-left)
    for r in range(rows - 3):
        for c in range(3, cols):
            if all(board[r+i][c-i] == symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    # No empty space in top row means Board is full
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHARS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_index]}'s turn to start!\n")

    while not game_over:
        print(f"Player {players[current_player_index]},", end=" ")
        col_index = get_valid_input(board)
        if col_index is not None:
            placed = place_checker(board, col_index, players[current_player_index])
            clear_screen()
            print_board(board)

            # Check for win
            if check_win(board, players[current_player_index]):
                print(f"Player {players[current_player_index]} won!")
                game_over = True
                continue

            # Check for draw
            if check_draw(board):
                print("It's a draw!")
                game_over = True
                continue

        else:
            clear_screen()
            print_board(board)

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
