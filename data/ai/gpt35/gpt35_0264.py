import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers A..G (or up to COLS)
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(headers)
    line = "+---" * len(board[0]) + "+"
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def is_valid_column(input_str, cols):
    if len(input_str) != 1:
        return False
    c = input_str[0]
    if not ('A' <= c <= chr(ord('A') + cols - 1)):
        return False
    return True

def column_to_index(col_char):
    return ord(col_char) - ord('A')

def place_checker(board, col, checker):
    # Place checker in the lowest empty spot of the column
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Column full

def check_win(board, last_row, last_col, checker):
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    nrows = len(board)
    ncols = len(board[0])

    for dr, dc in directions:
        count = 1

        # Check one direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < nrows and 0 <= c < ncols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check opposite direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < nrows and 0 <= c < ncols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True
    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        return
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column:")

        # Input validation loop
        while True:
            user_input = input().strip().upper()
            if not is_valid_column(user_input, COLS):
                print("Invalid input. Please enter a valid column letter:")
                continue

            col_idx = column_to_index(user_input)

            # Check if column full
            if board[0][col_idx] != " ":
                # Player loses turn if column full
                break

            # Place checker
            pos = place_checker(board, col_idx, current_checker)
            if pos is None:
                # Should not happen because we checked above
                print("Column full. You lose your turn.")
                break

            last_row, last_col = pos
            break

        print_board(board)

        # If player didn't place because column full, lose turn
        if board[0][col_idx] == current_checker:
            # Check win
            if check_win(board, last_row, last_col, current_checker):
                print(f"Player {current_checker} won!")
                return
            # Check draw
            if check_draw(board):
                print("The game is a draw!")
                return

        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
