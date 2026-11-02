import os
import random
import string

# Constants (you can change these for testing; submission requires ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7  # maximum 26 (A-Z)
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
CONNECT_N = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, player_symbol=None):
    clear_screen()
    cols = len(board[0])
    # Header with column letters
    letters = list(string.ascii_uppercase[:cols])
    print("  " + "   ".join(letters))
    # Top border
    print("+---" * cols + "+")
    # Rows
    for r in range(len(board)):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+---" * cols + "+")
    if player_symbol is not None:
        print(f"Player {player_symbol}, please enter a column:")

def is_valid_column_letter(s, cols):
    if len(s) != 1:
        return False
    if s not in string.ascii_uppercase:
        return False
    idx = ord(s) - ord('A')
    return 0 <= idx < cols

def find_drop_row(board, col):
    # Return the row index where the checker should land, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def drop_checker(board, col, symbol):
    r = find_drop_row(board, col)
    if r is None:
        return None
    board[r][col] = symbol
    return r

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win_from(board, r, c, dr, dc, symbol):
    rows = len(board)
    cols = len(board[0])
    for k in range(CONNECT_N):
        rr = r + dr * k
        cc = c + dc * k
        if not in_bounds(rr, cc, rows, cols):
            return False
        if board[rr][cc] != symbol:
            return False
    return True

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])
    # Directions: right, down, down-right, up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                if check_win_from(board, r, c, dr, dc, symbol):
                    return True
    return False

def check_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    # Setup and validation for constants
    if COLS < 1 or COLS > 26:
        raise ValueError("COLS must be between 1 and 26.")
    if ROWS < 1:
        raise ValueError("ROWS must be at least 1.")
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly choose first player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Print initial empty board
    print_board(board, players[current_player_index])

    while True:
        player_symbol = players[current_player_index]

        # Get a valid input (uppercase letter within range). Invalid inputs are retried.
        while True:
            user_input = input().strip()
            if is_valid_column_letter(user_input, COLS):
                col = ord(user_input) - ord('A')
                break
            else:
                print("Invalid input. Please enter a valid uppercase column letter (e.g., A, B, C).")

        # Attempt to drop checker
        placed_row = drop_checker(board, col, player_symbol)

        if placed_row is None:
            # Column full -> turn is invalid and player loses the turn
            print_board(board)  # Board unchanged but still reprinted
            print(f"Column {user_input} is full. Player {player_symbol} loses the turn.")
            input("Press Enter to continue...")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board, players[current_player_index])
            continue
        else:
            # Successful move: check for win, draw, or continue
            if check_win(board, player_symbol):
                print_board(board)
                print(f"Player {player_symbol} won!")
                break
            elif check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            else:
                # Next player's turn
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
                print_board(board, players[current_player_index])

if __name__ == "__main__":
    main()
