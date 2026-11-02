import os
import random
import string

# Constants (can be changed for custom configuration)
NUM_ROWS = 6
NUM_COLS = 7        # Max 26
NUM_PLAYERS = 2     # Between 2 and 5

PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

EMPTY_CELL = " "

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print the column headers (A-G, etc.)
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def is_valid_column(col_input, board):
    if len(col_input) != 1 or not col_input.isalpha() or not col_input.isupper():
        return False
    idx = ord(col_input) - ord('A')
    if idx < 0 or idx >= len(board[0]):
        return False
    # Check if there is any empty space in this column
    return board[0][idx] == EMPTY_CELL

def get_column_index(col_input):
    return ord(col_input) - ord('A')

def place_checker(board, col_idx, symbol):
    # Place from the bottom up
    for row in reversed(board):
        if row[col_idx] == EMPTY_CELL:
            row[col_idx] = symbol
            return board.index(row), col_idx  # Return the row and col of the placed checker
    return None, None  # Column full

def check_winner(board, row_idx, col_idx, symbol):
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1

        # Check in the positive direction
        r, c = row_idx + dr, col_idx + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc

        # Check in the negative direction
        r, c = row_idx - dr, col_idx - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True
    return False

def is_board_full(board):
    return all(cell != EMPTY_CELL for cell in board[0])

def get_player_input(player, board):
    while True:
        col_input = input(f"Player {player} ({player}), please enter a column: ").strip().upper()
        if not is_valid_column(col_input, board):
            print("Invalid input. Please enter a valid column (A-%s) that is not full." % string.ascii_uppercase[len(board[0])-1])
            continue
        return col_input

def main():
    random.seed()  # For true randomness
    board = create_board(NUM_ROWS, NUM_COLS)
    first_player_idx = random.randint(0, NUM_PLAYERS - 1)
    player_symbols = PLAYER_SYMBOLS
    turn = first_player_idx

    clear_screen()
    print_board(board)

    while True:
        current_player_idx = turn % NUM_PLAYERS
        current_symbol = player_symbols[current_player_idx]
        print()
        print(f"Player {current_symbol}, it's your turn.")
        col_input = get_player_input(current_symbol, board)
        col_idx = get_column_index(col_input)
        row_idx, actual_col_idx = place_checker(board, col_idx, current_symbol)

        clear_screen()
        print_board(board)

        if row_idx is not None and check_winner(board, row_idx, actual_col_idx, current_symbol):
            print(f"Player {current_symbol} won!")
            break
        elif is_board_full(board):
            print("The game is a draw!")
            break

        turn += 1

if __name__ == "__main__":
    main()
