import os
import random
import sys

# Constants
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
VALID_COLUMNS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  "
    for i in range(len(board[0])):
        header += "  " + chr(ord('A') + i) + " "
    print(header)
    # Print board cells with separators
    line = "+---" * len(board[0]) + "+"
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def get_next_player_index(current_index, num_players):
    return (current_index + 1) % num_players

def is_valid_input(user_input, board):
    if len(user_input) != 1:
        return False
    if user_input not in VALID_COLUMNS:
        return False
    col_idx = ord(user_input) - ord('A')
    # If the top row in that column is not empty, column is full
    if board[0][col_idx] != " ":
        return False
    return True

def place_checker(board, col_idx, checker):
    # Place checker in the lowest available row in column col_idx
    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx
    # Column full - should not place, but handle safely
    return None

def check_winner(board, last_row, last_col, checker):
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # Count last placed checker itself
        # Check in positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def check_draw(board):
    # If no empty space in top row, board is full (since pieces fill from bottom)
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    # Settings for submission requirements:
    num_players = 2
    rows = ROWS
    cols = COLUMNS

    players = PLAYERS[:num_players]

    board = create_board(rows, cols)
    current_player_idx = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        # Input loop - validate before placing
        while True:
            print(f"Player {current_checker}, please enter a column:")
            user_input = input().strip().upper()
            if user_input == "":  # Avoid empty input
                continue
            if len(user_input) != 1 or user_input not in VALID_COLUMNS:
                # invalid character or outside columns
                continue
            col_idx = ord(user_input) - ord('A')
            if board[0][col_idx] != " ":
                # full column;
                # player loses turn if column full as per assignment
                break
            # valid input & column not full
            break

        # If input invalid (not in columns) try again until valid
        # Here we only break if column is full (player loses turn)
        if len(user_input) != 1 or user_input not in VALID_COLUMNS or board[0][col_idx] != " ":
            # column full, players loses turn without placing
            print_board(board)
            current_player_idx = get_next_player_index(current_player_idx, num_players)
            continue

        # Place checker
        placed_row = place_checker(board, col_idx, current_checker)
        print_board(board)

        # Check for win
        if placed_row is not None:
            if check_winner(board, placed_row, col_idx, current_checker):
                print(f"Player {current_checker} won!")
                break

        # Check for draw
        if check_draw(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = get_next_player_index(current_player_idx, num_players)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame exited.")
        sys.exit(0)
