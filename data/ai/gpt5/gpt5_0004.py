import os
import random
import string

# Constants (submission requires 6x7 board and 2 players)
ROWS = 6
COLS = 7  # Max 26 columns
NUM_PLAYERS = 2  # Supports 2 to 5 players
WIN_LEN = 4

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    # As per assignment requirement (Linux/Unix)
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = list(string.ascii_uppercase[:cols])
    header = "  " + "   ".join(letters)
    sep = "+" + "+".join(["---"] * cols) + "+"

    clear_screen()
    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep)

def get_players(num_players):
    if num_players < 2 or num_players > 5:
        raise ValueError("Number of players must be between 2 and 5.")
    return PLAYER_SYMBOLS[:num_players]

def column_from_input(inp, cols):
    inp = inp.strip().upper()
    if len(inp) != 1:
        return None
    if inp < 'A' or inp > chr(ord('A') + cols - 1):
        return None
    return ord(inp) - ord('A')

def place_checker(board, col, symbol):
    # Place in the lowest available row in the given column
    # Returns True if placed, False if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return True
    return False

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 0
                rr, cc = r, c
                while count < WIN_LEN and in_bounds(rr, cc, rows, cols) and board[rr][cc] == symbol:
                    count += 1
                    rr += dr
                    cc += dc
                if count == WIN_LEN:
                    return True
    return False

def is_draw(board):
    # Draw if no spaces left anywhere
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def next_player_index(current, total):
    return (current + 1) % total

def main():
    # Validate column limit
    if COLS > 26:
        raise ValueError("Maximum of 26 columns supported (A-Z).")

    board = create_board(ROWS, COLS)
    players = get_players(NUM_PLAYERS)

    # Random starting player
    current_player_idx = random.randrange(0, len(players))

    # Show initial empty board before the game starts
    print_board(board)

    # Game loop
    while True:
        current_symbol = players[current_player_idx]
        # Prompt input until valid column letter within range
        while True:
            col_input = input(f"Player {current_symbol}, please enter a column: ")
            col = column_from_input(col_input, COLS)
            if col is None:
                print(f"Invalid input. Enter a letter from A to {chr(ord('A') + COLS - 1)}.")
                continue
            break

        # Try to place checker
        placed = place_checker(board, col, current_symbol)
        # Print updated board every turn (whether successful or not)
        print_board(board)

        if not placed:
            print(f"Column {chr(ord('A') + col)} is full. Turn lost.")
            # Turn lost, go to next player
            current_player_idx = next_player_index(current_player_idx, len(players))
            continue

        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, len(players))

if __name__ == "__main__":
    main()
