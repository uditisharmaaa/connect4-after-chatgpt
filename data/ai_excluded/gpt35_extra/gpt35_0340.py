import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players; use first PLAYERS of these
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels (A, B, C, ...)
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    # Print the board rows
    for row in board:
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))

def get_valid_column_input(board, player):
    cols = len(board[0])
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in col_labels:
            # Invalid input: must be a single valid column letter
            continue
        col_idx = ord(col_input) - ord('A')
        # Check if column is not full
        if board[0][col_idx] != " ":
            # Column full, player loses the turn
            return None
        return col_idx

def place_checker(board, col_idx, checker):
    # Place checker in lowest empty spot in column col_idx
    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return (row_idx, col_idx)  # Return where checker placed
    # Column full, should never reach here if input validated
    return None

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    r, c = start_row, start_col
    rows = len(board)
    cols = len(board[0])
    # Count consecutive checkers matching 'checker' going in delta direction
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    return count

def check_win(board, row, col, checker):
    # Check all directions for 4 in a row including the placed checker at (row,col)
    # Directions to check: horizontal, vertical, diagonal / and diagonal \
    directions = [
        ((0, -1), (0, 1)),    # horizontal left & right
        ((-1, 0), (1, 0)),    # vertical up & down
        ((-1, -1), (1, 1)),   # diagonal \
        ((-1, 1), (1, -1)),   # diagonal /
    ]
    for (d1, d2) in directions:
        dir1_count = check_direction(board, row, col, d1[0], d1[1], checker) - 1  # subtract 1 for double count
        dir2_count = check_direction(board, row, col, d2[0], d2[1], checker)
        if dir1_count + dir2_count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    # If top row is full, board is full (since we can't drop anymore)
    return all(cell != " " for cell in board[0])

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        col_idx = get_valid_column_input(board, player_checker)

        if col_idx is None:
            # Column full - lose turn, just print board and continue
            print_board(board)
            current_player_idx = (current_player_idx + 1) % PLAYERS
            continue

        placed = place_checker(board, col_idx, player_checker)
        print_board(board)

        if check_win(board, placed[0], placed[1], player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("The game is a draw.")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
