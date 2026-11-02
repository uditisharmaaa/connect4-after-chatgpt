import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print(" ", end=" ")
    for label in COLUMN_LABELS:
        print(f" {label}  ", end="")
    print()
    # Print top border
    print("+" + "---+" * COLUMNS)
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "---+" * COLUMNS)

def is_valid_column_input(input_str):
    if len(input_str) != 1:
        return False
    if input_str not in COLUMN_LABELS:
        return False
    return True

def get_column_index(column_letter):
    return ord(column_letter) - ord('A')

def place_checker(board, col, checker):
    # from bottom row to top, find first empty spot in column
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    # column full
    return -1

def check_win(board, row, col, checker):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        [(0, 1), (0, -1)],      # Horizontal right and left
        [(1, 0), (-1, 0)],      # Vertical down and up
        [(1, 1), (-1, -1)],     # Diagonal down-right and up-left
        [(1, -1), (-1, 1)]      # Diagonal down-left and up-right
    ]

    for direction in directions:
        count = 1  # Count includes just placed checker
        for d in direction:
            dr, dc = d
            r, c = row + dr, col + dc
            while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                count += 1
                r += dr
                c += dc
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randrange(NUM_PLAYERS)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")
        player_input = input().strip().upper()

        if not is_valid_column_input(player_input):
            # Invalid input, ask again without losing turn
            continue

        col = get_column_index(player_input)
        placed_row = place_checker(board, col, current_checker)
        if placed_row == -1:
            # Column full, player loses turn
            # do not ask for re-entry, just change turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Check win
        if check_win(board, placed_row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
