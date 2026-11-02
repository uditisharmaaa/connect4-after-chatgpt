import os
import random
import string

# ==== CONSTANTS ====
NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26  # For labeling with single letters (A-Z)
NUM_PLAYERS = 2  # For submission, set to 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Support up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    # Create a 2D board filled with " " (whitespace)
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    col_headers = "  " + "   ".join(string.ascii_uppercase[:NUM_COLS])
    print(col_headers)
    print("+" + "---+" * NUM_COLS)
    for row in board:
        row_str = "| " + " | ".join(row) + " |"
        print(row_str)
        print("+" + "---+" * NUM_COLS)

def get_valid_columns():
    return list(string.ascii_uppercase[:NUM_COLS])

def get_player_checker(player_idx):
    return PLAYER_CHECKERS[player_idx]

def is_column_full(board, col_idx):
    return board[0][col_idx] != " "

def get_next_open_row(board, col_idx):
    # Return the last row index that is empty in given column; else None
    for row in reversed(range(NUM_ROWS)):
        if board[row][col_idx] == " ":
            return row
    return None

def drop_checker(board, row, col, checker):
    board[row][col] = checker

def input_column(board, player_checker):
    valid_columns = get_valid_columns()
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Validate if input is a single letter in valid columns
        if len(user_input) != 1 or user_input not in valid_columns:
            print(f"Invalid input. Please enter a column letter (A-{valid_columns[-1]}).")
            continue
        col_idx = valid_columns.index(user_input)
        if is_column_full(board, col_idx):
            print(f"Column {user_input} is full! You lose your turn.")
            return None  # Lose the turn
        return col_idx

def check_victory(board, checker):
    # Check horizontal |
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical |
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (/)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (\)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    return False

def board_full(board):
    return all(board[0][col] != " " for col in range(NUM_COLS))

def main():
    # Randomly pick starting player
    player_indices = list(range(NUM_PLAYERS))
    current_player = random.choice(player_indices)

    # Initialize board
    board = create_board(NUM_ROWS, NUM_COLS)

    while True:
        clear_screen()
        print_board(board)
        player_checker = get_player_checker(current_player)
        col_idx = input_column(board, player_checker)
        if col_idx is None:  # Invalid move due to full column; skip turn
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        row_idx = get_next_open_row(board, col_idx)
        drop_checker(board, row_idx, col_idx, player_checker)

        # Check for win
        if check_victory(board, player_checker):
            clear_screen()
            print_board(board)
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
