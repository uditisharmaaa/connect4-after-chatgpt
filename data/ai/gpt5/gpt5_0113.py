import os
import random

# Constants (you can change ROWS, COLS, NUM_PLAYERS for testing; max COLS is 26)
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # between 2 and 5

# Checkers in order for up to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]

# Ensure constraints
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if COLS > 26 or COLS < 1:
    raise ValueError("COLS must be between 1 and 26.")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")

PLAYERS = CHECKERS[:NUM_PLAYERS]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_and_print_board(board):
    os.system('clear')
    # Print header with column letters
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    header = "  " + "   ".join(letters)
    print(header)
    # Print grid
    sep = "+" + "+".join(["---"] * len(board[0])) + "+"
    for r in range(len(board)):
        print(sep)
        row_str = "|"
        for c in range(len(board[0])):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(sep)

def get_valid_column_input(cols):
    while True:
        user_in = input("Please enter a column (A-{}): ".format(chr(ord('A') + cols - 1))).strip()
        if not user_in:
            print("Invalid input. Try again.")
            continue
        user_in = user_in.upper()
        if len(user_in) != 1 or not ('A' <= user_in <= chr(ord('A') + cols - 1)):
            print("Invalid input. Enter a single letter between A and {}.".format(chr(ord('A') + cols - 1)))
            continue
        return ord(user_in) - ord('A')

def drop_checker(board, col, checker):
    # Place checker in the lowest available row in the given column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None  # Column full

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def count_in_direction(board, start_r, start_c, dr, dc, checker):
    count = 0
    r, c = start_r, start_c
    rows = len(board)
    cols = len(board[0])
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, last_r, last_c, checker):
    # Check all directions through the last placed checker
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        # Count both ways from the last position (avoid double counting center)
        total = 1
        total += count_line(board, last_r, last_c, dr, dc, checker)
        total += count_line(board, last_r, last_c, -dr, -dc, checker)
        if total >= 4:
            return True
    return False

def count_line(board, r, c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    cnt = 0
    nr = r + dr
    nc = c + dc
    while in_bounds(nr, nc, rows, cols) and board[nr][nc] == checker:
        cnt += 1
        nr += dr
        nc += dc
    return cnt

def is_draw(board):
    for r in board:
        if " " in r:
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Show initial empty board and randomly chosen first player
    clear_and_print_board(board)
    print("Player {}, you start!".format(PLAYERS[current_player_index]))

    while True:
        clear_and_print_board(board)
        current_checker = PLAYERS[current_player_index]
        print("Player {}, please enter a column:".format(current_checker))

        col = get_valid_column_input(COLS)

        result = drop_checker(board, col, current_checker)
        if result is None:
            # Column full: turn is invalid and player loses the turn
            print("Column {} is full. Turn lost!".format(chr(ord('A') + col)))
            input("Press Enter to continue...")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        last_r, last_c = result

        # Check for a win
        if check_win(board, last_r, last_c, current_checker):
            clear_and_print_board(board)
            print("Player {} won!".format(current_checker))
            break

        # Check for a draw
        if is_draw(board):
            clear_and_print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
