import os
import random

# Constants (you may change these for testing, but submit with ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Supported range: 2 to 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Used in order

# Ensure limits
COLS = max(1, min(26, COLS))
NUM_PLAYERS = max(2, min(5, NUM_PLAYERS))
SYMBOLS = PLAYER_SYMBOLS[:NUM_PLAYERS]

def clear_screen():
    try:
        os.system('clear')
    except Exception:
        pass

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column labels
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    line = "+" + ("---+" * cols)

    print(header)
    for r in range(rows):
        print(line)
        row_str = ""
        for c in range(cols):
            row_str += f"| {board[r][c]} "
        row_str += "|"
        print(row_str)
    print(line)

def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def place_checker(board, col, symbol):
    # Place in the lowest available row in the given column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r, col
    return None  # Column is full

def check_winner(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Directions: right, down, down-right, up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    for r in range(rows):
        for c in range(cols):
            sym = board[r][c]
            if sym == " ":
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r, c
                for _ in range(3):
                    rr += dr
                    cc += dc
                    if 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == sym:
                        count += 1
                    else:
                        break
                if count == 4:
                    return sym
    return None

def get_valid_column_input(cols):
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Enter a single letter corresponding to a column.")
            continue
        ch = user_input[0]
        if not ('A' <= ch <= chr(ord('A') + cols - 1)):
            print("Invalid column letter. Try again.")
            continue
        return ord(ch) - ord('A')

def main():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)
    print(f"Player {SYMBOLS[current_player]}, you start.")

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {SYMBOLS[current_player]},", end=" ")

        col = get_valid_column_input(COLS)

        result = place_checker(board, col, SYMBOLS[current_player])
        if result is None:
            # Column full: lose the turn
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {SYMBOLS[current_player]} loses the turn.")
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS
            # Continue to next loop iteration
            if is_board_full(board):
                clear_screen()
                print_board(board)
                print("It's a draw!")
                break
            continue

        # Check for win
        winner = check_winner(board)
        if winner is not None:
            clear_screen()
            print_board(board)
            print(f"Player {winner} won!")
            break

        # Check for draw
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
