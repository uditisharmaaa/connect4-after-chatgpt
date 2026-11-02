import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

# Set game configuration
NUM_PLAYERS = 2  # Between 2 and 5
PLAYER_CHECKERS = PLAYERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column labels (A-G)
    header = "  "
    for i in range(cols):
        header += f"  {chr(ord('A') + i)} "
    print(header)
    # Print board rows with horizontal lines
    line = "+" + "---+" * cols
    for r in range(rows):
        print(line)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(line)

def input_column(prompt, board):
    cols = len(board[0])
    while True:
        user_input = input(prompt).strip().upper()
        # Validate single uppercase letter in the board columns range
        if len(user_input) != 1:
            print("Invalid input. Enter a single column letter.")
            continue
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= cols:
            print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + cols - 1)}.")
            continue
        # Check if column already full; if full player loses turn (return None)
        if board[0][col_index] != " ":
            # According to instructions: "If the column is already completely filled with checkers,
            # the turn is invalid and the player loses the turn."
            return None
        return col_index

def place_checker(board, col, checker):
    # Find from bottom row up first empty space in the column
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    # If no spot found (should not happen if called properly)
    return None

def check_winner(board, last_row, last_col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_dir(dr, dc):
        count = 0
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # Directions: horizontal, vertical, diagonal(/), diagonal(\)
    directions = [
        ((0, -1), (0, 1)),   # Horizontal left and right
        ((-1, 0), (1, 0)),   # Vertical up and down
        ((-1, -1), (1, 1)),  # Diagonal top-left to bottom-right
        ((-1, 1), (1, -1)),  # Diagonal top-right to bottom-left
    ]

    for (d1, d2) in directions:
        count = 1  # count the placed checker itself
        count += count_dir(*d1)
        count += count_dir(*d2)
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    # If top row has no spaces, board is full
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player_index]} will start.")

    while True:
        checker = PLAYER_CHECKERS[current_player_index]
        prompt = f"Player {checker}, please enter a column: "
        col = input_column(prompt, board)
        if col is None:
            # column full - turn lost
            print(f"Column is full. Player {checker} loses the turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        placed = place_checker(board, col, checker)
        print_board(board)
        if placed is None:
            # Should not happen, but just in case
            print(f"Error: could not place checker for player {checker}. Turn lost.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        last_row, last_col = placed
        if check_winner(board, last_row, last_col, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
