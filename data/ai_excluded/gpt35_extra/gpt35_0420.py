import os
import random
import string

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # max 5 players
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers A, B, C...
    header = "  " + "   ".join(string.ascii_uppercase[:COLS])
    print(header)
    # print rows
    sep = "+---" * COLS + "+"
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    if col_char not in string.ascii_uppercase[:COLS]:
        return False
    return True

def get_column_index(col_char):
    return ord(col_char) - ord('A')

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place checker at lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full
    return None

def check_win(board, checker, row, col):
    # Directions to check (dx, dy)
    directions = [
        (0, 1),  # vertical down
        (1, 0),  # horizontal right
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]

    for dx, dy in directions:
        count = 1
        # Check in positive direction
        r, c = row + dy, col + dx
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dy
            c += dx
        # Check in negative direction
        r, c = row - dy, col - dx
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dy
            c -= dx
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for col in range(COLS):
        if not is_column_full(board, col):
            return False
    return True

def get_valid_input(current_player_checker):
    while True:
        inp = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(inp):
            continue
        col = get_column_index(inp)
        return col

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        return
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]

        col = get_valid_input(current_checker)

        if is_column_full(board, col):
            # Player loses turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        pos = place_checker(board, col, current_checker)
        print_board(board)
        if pos is None:
            # Should not happen because we checked column full before
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        row_placed, col_placed = pos
        if check_win(board, current_checker, row_placed, col_placed):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("The game is a draw.")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
