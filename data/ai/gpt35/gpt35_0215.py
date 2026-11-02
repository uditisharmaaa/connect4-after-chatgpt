import os
import random
import string

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers A, B, C ...
    header = "  "
    for col in range(cols):
        header += "  {} ".format(string.ascii_uppercase[col])
    print(header)
    # Print separator line
    line = "+---" * cols + "+"
    for row in range(len(board)):
        print(line)
        row_str = "|"
        for col in range(cols):
            row_str += " {} |".format(board[row][col])
        print(row_str)
    print(line)

def get_valid_column_input(board, current_player):
    cols = len(board[0])
    col_letters = string.ascii_uppercase[:cols]
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip()
        if len(user_input) != 1:
            # length not 1
            continue
        if user_input not in col_letters:
            continue
        col_index = col_letters.index(user_input)
        # Check if column is full
        if board[0][col_index] != " ":
            # Column full => player loses turn
            return None
        return col_index

def place_checker(board, column, checker):
    # From bottom row upwards find the first empty space
    for row in range(len(board)-1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return row, column
    return None  # Should never happen if we checked column full before

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    # Directions as pairs of increments: (delta_row, delta_col)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # count includes the placed checker

        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True

    return False

def check_draw(board):
    # If top row for every column is occupied, board is full
    return all(cell != " " for cell in board[0])

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]

    # Random player starts
    current_index = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        current_player = players[current_index]
        col_index = get_valid_column_input(board, current_player)
        if col_index is None:
            # Player loses turn if column full
            current_index = (current_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        row, col = place_checker(board, col_index, current_player)
        print_board(board)

        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw.")
            break

        current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
