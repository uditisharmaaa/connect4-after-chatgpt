import os
import random

# =================== CONSTANTS ====================
ROWS = 6                    # Number of board rows
COLUMNS = 7                 # Number of board columns, max 26
NUM_PLAYERS = 2             # Number of players (2-5)
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols

COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

# =================== FUNCTIONS ====================

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    # Print column headers
    print("  " + "   ".join(COLUMN_LABELS))
    # Print top border
    print("+" + "---+" * COLUMNS)
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_next_open_row(board, col):
    # Return the index of the lowest empty row in the given column, or -1 if full
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1

def is_valid_column(col_str):
    # Check input is a single letter and is on the board
    return len(col_str) == 1 and col_str in COLUMN_LABELS

def check_winner(board, row, col, checker):
    # Check all 4 directions for a win starting from (row, col)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # check forwards
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # check backwards
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_board_full(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def switch_player(current):
    return (current + 1) % NUM_PLAYERS

def main():
    # Setup
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS-1)

    # Game start
    clear_screen()
    print("Welcome to Connect 4!")
    print(f"Players: {' '.join(PLAYER_CHECKERS)}")
    print(f"First player: {PLAYER_CHECKERS[current_player]}")
    print_board(board)

    while True:
        player_checker = PLAYER_CHECKERS[current_player]
        print(f"Player {player_checker}, please enter a column:")

        # Input loop for valid input
        while True:
            col_input = input().strip().upper()
            if not is_valid_column(col_input):
                print(f"Invalid input. Please enter a column letter from A to {COLUMN_LABELS[-1]}:")
                continue
            col = ord(col_input) - ord('A')
            open_row = get_next_open_row(board, col)
            if open_row == -1:
                print("Column is full. You lose your turn.")
                open_row = None
            break

        # If column is full, skip turn
        if open_row is None:
            current_player = switch_player(current_player)
            clear_screen()
            print_board(board)
            continue

        # Place checker
        board[open_row][col] = player_checker

        clear_screen()
        print_board(board)

        # Check winner
        if check_winner(board, open_row, col, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check draw
        if is_board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = switch_player(current_player)

if __name__ == "__main__":
    main()
