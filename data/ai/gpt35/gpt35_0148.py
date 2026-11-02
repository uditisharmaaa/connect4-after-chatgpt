import os
import random
import string

# Constants for the board dimensions and players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Support up to 5 players
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    col_labels = string.ascii_uppercase[:len(board[0])]
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def valid_column_input(col_str, cols):
    if len(col_str) != 1:
        return False
    if col_str not in string.ascii_uppercase[:cols]:
        return False
    return True

def get_column_index(col_str):
    return ord(col_str) - ord('A')

def place_checker(board, col_idx, checker):
    # Place checker in lowest available row in column, if any
    for row_idx in reversed(range(len(board))):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx
    # Column full
    return -1

def check_winner(board, last_row, last_col, checker):
    # Directions: horizontal, vertical, diagonal /, diagonal \
    directions = [
        (0, 1),  # Horizontal right
        (1, 0),  # Vertical down
        (1, 1),  # Diagonal down-right
        (1, -1), # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # Count the checker at last placed position
        # Check forward direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    active_players = PLAYERS[:NUM_PLAYERS]

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        checker = active_players[current_player_index]
        # Input loop for valid column
        while True:
            col_input = input(f"Player {checker}, please enter a column: ").upper()
            if not valid_column_input(col_input, COLS):
                # Invalid input, ask again
                continue
            col_idx = get_column_index(col_input)
            placed_row = place_checker(board, col_idx, checker)
            if placed_row == -1:
                # Column full: turn lost
                break
            else:
                # Valid placement, break input loop
                break

        print_board(board)

        if placed_row != -1:
            # Check for winning condition
            if check_winner(board, placed_row, col_idx, checker):
                print(f"Player {checker} won!")
                return
        else:
            # Column full - turn lost, but still need to check draw
            pass

        if board_full(board):
            print("The game is a draw!")
            return

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
