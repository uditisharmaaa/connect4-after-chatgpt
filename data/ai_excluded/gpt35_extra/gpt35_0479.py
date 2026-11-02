import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LENGTH = 4
COLUMN_LABELS = string.ascii_uppercase[:COLUMNS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print rows
    for row in range(ROWS):
        print("+" + "---+" * COLUMNS)
        row_str = "|"
        for col in range(COLUMNS):
            row_str += " {} |".format(board[row][col])
        print(row_str)
    print("+" + "---+" * COLUMNS)

def get_player_input(player_checker, board):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input not in COLUMN_LABELS:
            # Invalid input: must be single uppercase letter in range
            print(f"Invalid input. Please enter a column letter between A and {COLUMN_LABELS[-1]}.")
            continue
        col_index = COLUMN_LABELS.index(user_input)
        # Check if column is full
        if board[0][col_index] != " ":
            # Column full, turn lost
            return None
        return col_index

def place_checker(board, col, player_checker):
    # Place checker in lowest available space in column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return row, col
    # Should never hit here if checked before
    return None, None

def check_win(board, player_checker, row, col):
    # Directions to check: horizontal, vertical, diag up-right, diag down-right
    directions = [
        (0, 1),  # Horizontal right
        (1, 0),  # Vertical down
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def check_draw(board):
    # If all top cells are filled and no winner => draw
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    current_idx = random.randint(0, NUM_PLAYERS -1)
    num_moves = 0

    print_board(board)
    while True:
        player_checker = CHECKERS[current_idx]
        col = get_player_input(player_checker, board)
        if col is None:
            # Column full, lose turn
            print(f"Column is full. Player {player_checker} loses turn.")
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue
        row, col = place_checker(board, col, player_checker)
        num_moves += 1
        print_board(board)
        # Check win
        if check_win(board, player_checker, row, col):
            print(f"Player {player_checker} won!")
            break
        # Check draw
        if check_draw(board):
            print("Game is a draw!")
            break
        # Next player
        current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
