import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(headers))
    # Print board rows
    row_sep = "+---" * len(board[0]) + "+"
    for row in board:
        print(row_sep)
        print("| " + " | ".join(row) + " |")
    print(row_sep)

def input_column(player_checker, board):
    cols = len(board[0])
    valid_columns = [chr(ord('A') + i) for i in range(cols)]
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Validate input character(s)
        if len(col_input) != 1 or col_input not in valid_columns:
            continue  # invalid input, ask again
        
        col_index = ord(col_input) - ord('A')
        # Check if column is full
        if board[0][col_index] != " ":
            # Column full, player loses turn (per assignment)
            return None
        return col_index

def place_checker(board, col_index, checker):
    # Start from bottom row and find first empty slot
    for row_i in reversed(range(len(board))):
        if board[row_i][col_index] == " ":
            board[row_i][col_index] = checker
            return row_i, col_index
    return None  # Should never reach here if checked previously

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row = start_row
    col = start_col
    rows = len(board)
    cols = len(board[0])
    while 0 <= row < rows and 0 <= col < cols and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, row, col, checker):
    # Directions: horizontal, vertical, diagonal /
    # diag1 is top-left to bottom-right, diag2 is bottom-left to top-right
    directions = [
        ((0, -1), (0, 1)),    # horizontal left, right
        ((-1, 0), (1, 0)),    # vertical up, down
        ((-1, -1), (1, 1)),   # diagonal \
        ((1, -1), (-1, 1))    # diagonal /
    ]
    for (d1, d2) in directions:
        count = 1  # count the starting checker
        count += check_direction(board, row + d1[0], col + d1[1], d1[0], d1[1], checker)
        count += check_direction(board, row + d2[0], col + d2[1], d2[0], d2[1], checker)
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    # Initialize
    board = create_board(ROWS, COLS)
    player_order = list(range(PLAYERS))
    random.shuffle(player_order)
    # Player checkers assigned in order 0..PLAYERS-1
    player_checkers = CHECKERS[:PLAYERS]
    current_player_idx = 0
    # Find starting player after shuffle
    current_player_idx = 0  
    current_player = player_order[current_player_idx]

    print_board(board)

    while True:
        checker = player_checkers[current_player]
        col = None
        col = input_column(checker, board)
        if col is None:
            # Column full, turn lost
            current_player_idx = (current_player_idx + 1) % PLAYERS
            current_player = player_order[current_player_idx]
            print_board(board)
            continue  # Next player's turn

        pos = place_checker(board, col, checker)
        print_board(board)

        row, col_placed = pos
        if check_win(board, row, col_placed, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS
        current_player = player_order[current_player_idx]

if __name__ == "__main__":
    main()
