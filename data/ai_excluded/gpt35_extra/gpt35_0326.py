import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = "  "
    for c in range(COLS):
        headers += "  " + chr(ord('A') + c) + " "
    print(headers)
    # Print top border
    print("+" + "---+" * COLS)
    # Print each row
    for r in range(ROWS):
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print("+" + "---+" * COLS)

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    if 'A' <= col_char < chr(ord('A') + COLS):
        return True
    return False

def column_to_index(col_char):
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    # Start from bottom row, find first empty spot
    for row in range(ROWS-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    # Column full
    return None, None

def check_win(board, row, col, checker):
    # Check all directions from (row,col)
    # Return True if 4 in a row found for checker

    directions = [ 
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Count self
        # Check forwards
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backwards
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        checker = players[current_player_idx]
        print(f"Player {checker}, please enter a column:")
        input_valid = False
        col_idx = None

        # Input validation loop
        while not input_valid:
            user_input = input().strip()
            if not is_valid_column(user_input):
                print("Invalid input. Please enter a valid column letter:")
                continue

            col_idx = column_to_index(user_input)
            # Check if column is full
            if board[0][col_idx] != " ":
                # Turn lost if full
                print("Column is full. You lose your turn.")
                col_idx = None
                input_valid = True  # Accept input but place_checker won't place
            else:
                input_valid = True

        if col_idx is not None:
            row_placed, col_placed = place_checker(board, col_idx, checker)
            print_board(board)
            # Check win if checker placed
            if check_win(board, row_placed, col_placed, checker):
                print(f"Player {checker} won!")
                break
            # Check draw
            if board_full(board):
                print("The game is a draw!")
                break
        else:
            print_board(board)

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
