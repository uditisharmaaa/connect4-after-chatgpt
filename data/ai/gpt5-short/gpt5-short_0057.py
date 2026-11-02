import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2  # Change to 2..5 to choose how many players will play

# Make sure NUM_PLAYERS is valid
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("NUM_PLAYERS must be between 2 and 5. Defaulting to 2.")
    NUM_PLAYERS = 2

def clear_screen():
    # Clear the terminal
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board):
    # Print column labels
    print("  " + " ".join(COLUMN_LABELS))
    # Print rows from top to bottom
    for r in range(ROWS):
        line = "|"
        for c in range(COLS):
            line += board[r][c] + "|"
        print(line)
    print("-" * (COLS * 2 + 1))

def col_to_index(col_char):
    return ord(col_char) - ord('A')

def is_valid_column(board, col_idx):
    if col_idx < 0 or col_idx >= COLS:
        return False
    # A column is valid if the top cell is empty
    return board[0][col_idx] == ' '

def get_next_open_row(board, col_idx):
    # Start from bottom row and find first empty
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == ' ':
            return r
    return None

def drop_piece(board, row, col, symbol):
    board[row][col] = symbol

def check_win(board, symbol):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and
                board[r][c+1] == symbol and
                board[r][c+2] == symbol and
                board[r][c+3] == symbol):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == symbol and
                board[r+1][c] == symbol and
                board[r+2][c] == symbol and
                board[r+3][c] == symbol):
                return True

    # Check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and
                board[r+1][c+1] == symbol and
                board[r+2][c+2] == symbol and
                board[r+3][c+3] == symbol):
                return True

    # Check diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and
                board[r-1][c+1] == symbol and
                board[r-2][c+2] == symbol and
                board[r-3][c+3] == symbol):
                return True

    return False

def check_draw(board):
    # Draw if no empty spaces in top row
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def get_player_symbols():
    # Return first NUM_PLAYERS symbols from PLAYER_SYMBOLS
    return PLAYER_SYMBOLS[:NUM_PLAYERS]

def main():
    board = create_board()
    players = get_player_symbols()
    current_player_idx = random.randrange(len(players))

    while True:
        clear_screen()
        print_board(board)
        symbol = players[current_player_idx]
        print("Players:", " ".join(players))
        print("Current player:", symbol)

        # Get and validate input
        while True:
            choice = input("Choose a column (A-G): ").strip().upper()
            if len(choice) != 1 or choice not in COLUMN_LABELS:
                print("Invalid input. Enter a letter A-G.")
                continue

            col_idx = col_to_index(choice)
            if not is_valid_column(board, col_idx):
                print("That column is full. Try another.")
                continue
            break

        # Drop the piece
        row_idx = get_next_open_row(board, col_idx)
        drop_piece(board, row_idx, col_idx, symbol)

        # Check for win
        if check_win(board, symbol):
            clear_screen()
            print_board(board)
            print("Player", symbol, "wins!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % len(players)

if __name__ == "__main__":
    main()
