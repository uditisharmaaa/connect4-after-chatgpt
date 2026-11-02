import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]

EMPTY_CELL = " "

def clear_screen():
    os.system('clear')

def create_board():
    return [[EMPTY_CELL for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = "  "
    for c in range(COLS):
        headers += chr(ord('A') + c) + "   "
    print(headers)
    # Print rows with separators
    separator = "+" + "---+" * COLS
    for r in range(ROWS):
        print(separator)
        row = "|"
        for c in range(COLS):
            row += " " + board[r][c] + " |"
        print(row)
    print(separator)

def valid_column_input(input_str):
    if len(input_str) != 1:
        return False
    c = input_str[0]
    if 'A' <= c <= chr(ord('A') + COLS - 1):
        return True
    return False

def column_index(col_letter):
    return ord(col_letter) - ord('A')

def is_column_full(board, col):
    return board[0][col] != EMPTY_CELL

def place_checker(board, col, checker):
    # Bottom row is ROWS-1, place checker at lowest empty cell
    for row in reversed(range(ROWS)):
        if board[row][col] == EMPTY_CELL:
            board[row][col] = checker
            return row, col
    return -1, -1  # Column full, should be handled before

def check_win(board, row, col, checker):
    # Directions: horizontal, vertical, two diagonals
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Include the placed checker itself
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    for c in range(COLS):
        if not is_column_full(board, c):
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")
        user_input = input().strip().upper()

        # Input validation
        if not valid_column_input(user_input):
            continue  # Invalid input, ask again

        col = column_index(user_input)
        if is_column_full(board, col):
            # Turn lost if column full
            current_player_idx = (current_player_idx + 1) % PLAYERS
            continue

        # Place checker
        row, col = place_checker(board, col, current_checker)
        print_board(board)

        # Check win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if board_full(board):
            print("Game is a draw!")
            break

        # Next turn
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
