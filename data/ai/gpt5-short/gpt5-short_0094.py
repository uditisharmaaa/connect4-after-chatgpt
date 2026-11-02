import os
import random

# Constants you can change for your class
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Choose how many players (2 to 5). Players use these symbols in order:
ALL_PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # change to 3, 4, or 5 if you want more players

# Board cell for empty
EMPTY = '.'

def clear_screen():
    # Clears the screen (works on most Unix-like systems)
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = [EMPTY] * COLS
        board.append(row)
    return board

def print_board(board, players, current_player_index):
    # Header
    print("Connect 4 - {} players: {}".format(len(players), " ".join(players)))
    print("Current player: {}".format(players[current_player_index]))
    print()
    # Column labels
    print("  " + " ".join(COLUMN_LABELS))
    # Rows
    for r in range(ROWS):
        row_str = []
        for c in range(COLS):
            row_str.append(board[r][c])
        print("| " + " ".join(row_str))
    print()

def get_column_index_from_input(user_input):
    if len(user_input) != 1:
        return -1
    ch = user_input.upper()
    if ch in COLUMN_LABELS:
        return COLUMN_LABELS.index(ch)
    return -1

def drop_piece(board, col, symbol):
    # Drop from bottom up; return the row index where the piece lands, or -1 if column is full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = symbol
            return r
    return -1

def board_full(board):
    # If any cell on the top row is empty, board isn't full
    for c in range(COLS):
        if board[0][c] == EMPTY:
            return False
    return True

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
    for r in range(ROWS - 3):
        for c in range(COLS):
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

    # Check diagonal down-left
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if (board[r][c] == symbol and
                board[r+1][c-1] == symbol and
                board[r+2][c-2] == symbol and
                board[r+3][c-3] == symbol):
                return True

    return False

def get_valid_move(board, current_symbol):
    while True:
        user_input = input("Player {} - choose column (A-G): ".format(current_symbol)).strip()
        col = get_column_index_from_input(user_input)
        if col == -1:
            print("Invalid input. Enter a single letter A-G.")
            continue
        # Try to drop; if full, tell user and retry
        row = drop_piece(board, col, current_symbol)
        if row == -1:
            print("Column {} is full. Choose another.".format(COLUMN_LABELS[col]))
            continue
        return row, col  # successful move

def main():
    # Validate number of players
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return

    players = ALL_PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board()

    # Random first player
    current_player_index = random.randrange(len(players))

    while True:
        clear_screen()
        print_board(board, players, current_player_index)

        current_symbol = players[current_player_index]
        row, col = get_valid_move(board, current_symbol)

        # After a valid move, re-render
        clear_screen()
        print_board(board, players, current_player_index)

        # Check win or draw
        if check_win(board, current_symbol):
            print("Player {} wins!".format(current_symbol))
            break
        if board_full(board):
            print("It's a draw!")
            break

        # Next player
        current_player_index = (current_player_index + 1) % len(players)

    print("Game over.")

if __name__ == "__main__":
    main()
