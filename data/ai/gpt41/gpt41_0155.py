import os
import random
import string

# === CONSTANTS ===
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2    # Change to 2..5 as desired
PLAYER_CHARS = ["X", "O", "V", "H", "M"]    # Up to 5 players
COLUMN_LABELS = list(string.ascii_uppercase[:COLUMNS])

# === FUNCTIONS ===

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column letters
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_next_open_row(board, col):
    for row in range(ROWS-1, -1, -1):  # Start from bottom
        if board[row][col] == " ":
            return row
    return None  # Column is full

def is_column_full(board, col):
    return board[0][col] != " "

def board_full(board):
    for col in range(COLUMNS):
        if not is_column_full(board, col):
            return False
    return True

def is_winner(board, player_char):
    # Check horizontal locations
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_char for i in range(4)):
                return True

    # Check vertical locations
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_char for i in range(4)):
                return True

    # Check positively sloped diagonals (/)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_char for i in range(4)):
                return True

    # Check negatively sloped diagonals (\)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_char for i in range(4)):
                return True

    return False

def get_valid_column_input(board):
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in COLUMN_LABELS:
            print(f"Invalid input. Enter a letter A-{COLUMN_LABELS[-1]}.")
            continue
        col = COLUMN_LABELS.index(col_input)
        if is_column_full(board, col):
            print("Column is full! You lose your turn.")
            return None  # Lose turn as per rules
        return col

def main():
    board = create_board(ROWS, COLUMNS)
    active_players = PLAYER_CHARS[:NUM_PLAYERS]
    first_player = random.randint(0, NUM_PLAYERS - 1)
    curr_player_idx = first_player

    # Initial print
    print_board(board)
    print(f"Player {active_players[curr_player_idx]} was randomly selected to start.")

    game_over = False

    while not game_over:
        player_char = active_players[curr_player_idx]

        print_board(board)
        print(f"Player {player_char},", end=" ")

        col = get_valid_column_input(board)

        if col is not None:
            row = get_next_open_row(board, col)
            if row is not None:
                board[row][col] = player_char

                # Check for win
                if is_winner(board, player_char):
                    print_board(board)
                    print(f"Player {player_char} won!")
                    return

                # Check for draw
                if board_full(board):
                    print_board(board)
                    print("It's a draw!")
                    return

        # Next player
        curr_player_idx = (curr_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
