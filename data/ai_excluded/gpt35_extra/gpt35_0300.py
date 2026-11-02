import os
import random

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_CONDITION = 4

# Players tokens in order
PLAYERS_TOKENS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    sep = "+" + "---+" * len(board[0])
    print(header)
    print(sep)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(sep)

def get_player_input(player_token, board):
    cols = len(board[0])
    while True:
        inp = input(f"Player {player_token}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            continue
        col = ord(inp) - ord('A')
        if 0 <= col < cols:
            if board[0][col] == " ":  # Check if top cell is empty - column not full
                return col
            else:
                # Column full, lose turn
                return None
        # Invalid input, ask again

def place_checker(board, col, token):
    # Place token in the lowest empty row in the selected column
    for r in reversed(range(len(board))):
        if board[r][col] == " ":
            board[r][col] = token
            return r, col  # Return position of placed checker
    # If column full, should not reach here if logic correct
    return None

def check_win(board, token):
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == token for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == token for i in range(WIN_CONDITION)):
                return True

    # Check diagonal down-right
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == token for i in range(WIN_CONDITION)):
                return True

    # Check diagonal down-left
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(WIN_CONDITION - 1, cols):
            if all(board[r + i][c - i] == token for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    # Draw if no empty space in top row (means board full)
    return all(cell != " " for cell in board[0])

def main():
    rows = ROWS
    cols = COLS
    num_players = MIN_PLAYERS
    tokens = PLAYERS_TOKENS[:num_players]

    board = create_board(rows, cols)
    # Randomly select first player index
    current_player_idx = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        player_token = tokens[current_player_idx]
        col = get_player_input(player_token, board)

        if col is None:
            # Column full, player loses turn
            # Simply skip their turn, do not place checker
            current_player_idx = (current_player_idx + 1) % num_players
            print_board(board)
            continue

        row_col = place_checker(board, col, player_token)
        print_board(board)

        if check_win(board, player_token):
            print(f"Player {player_token} won!")
            break

        if check_draw(board):
            print("The game is a draw.")
            break

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
