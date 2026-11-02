import os
import random

# Constants (you may change these for testing; submission requires ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7  # Maximum 26
NUM_PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    # Clear terminal screen (Linux/Unix)
    os.system('clear')

def print_board(board):
    cols = len(board[0])
    # Header letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    # Separator
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(" " + board[r][c] + " ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)

def get_column_index_from_input(user_input, cols):
    s = user_input.strip().upper()
    if len(s) != 1:
        return None
    if not ('A' <= s <= 'Z'):
        return None
    idx = ord(s) - ord('A')
    if 0 <= idx < cols:
        return idx
    return None

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, token):
    # Place token in lowest available spot in the column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None  # Column full

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, token):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
                    count += 1
                    if count == 4:
                        return True
                    nr += dr
                    nc += dc
    return False

def is_draw(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    if COLS > 26:
        print("Error: Maximum supported columns is 26.")
        return
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: Number of players must be between 2 and 5.")
        return

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)
    current_player_idx = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)
        token = players[current_player_idx]

        # Prompt for input and validate
        while True:
            user_in = input(f"Player {token}, please enter a column: ")
            col_idx = get_column_index_from_input(user_in, COLS)
            if col_idx is None:
                print(f"Invalid input. Enter a letter between A and {chr(ord('A') + COLS - 1)}.")
                continue
            break

        # Attempt to place checker
        if is_column_full(board, col_idx):
            # Turn is invalid and the player loses the turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        row_placed = place_checker(board, col_idx, token)

        # Check for win
        if check_win(board, token):
            clear_screen()
            print_board(board)
            print(f"Player {token} won!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
