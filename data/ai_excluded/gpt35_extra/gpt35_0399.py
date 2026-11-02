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

def create_board(rows=ROWS, cols=COLS):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    # Print board rows and separators
    for row in range(len(board)):
        print("+" + "---+" * len(board[0]))
        line = "|"
        for col in range(len(board[0])):
            line += " " + board[row][col] + " |"
        print(line)
    print("+" + "---+" * len(board[0]))

def is_valid_input(inp, cols):
    if len(inp) != 1:
        return False
    if not ('A' <= inp <= chr(ord('A') + cols -1)):
        return False
    return True

def get_lowest_empty_row(board, col):
    # from bottom row to top row
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return -1

def place_checker(board, col, checker):
    row = get_lowest_empty_row(board, col)
    if row == -1:
        return False  # column full
    board[row][col] = checker
    return True

def check_direction(board, start_row, start_col, d_row, d_col, checker):
    count = 0
    r, c = start_row, start_col
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r += d_row
        c += d_col
    return count

def check_win(board, checker):
    # Check all positions on board for win starting at that position
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                # horizontal to right
                if check_direction(board, row, col, 0, 1, checker) >= WIN_COUNT:
                    return True
                # vertical down
                if check_direction(board, row, col, 1, 0, checker) >= WIN_COUNT:
                    return True
                # diagonal down-right
                if check_direction(board, row, col, 1, 1, checker) >= WIN_COUNT:
                    return True
                # diagonal down-left
                if check_direction(board, row, col, 1, -1, checker) >= WIN_COUNT:
                    return True
    return False

def check_draw(board):
    # If no spaces left in top row (or anywhere), it's a draw
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        checker = players_checkers[current_player_index]
        prompt = f"Player {checker}, please enter a column: "
        col_input = input(prompt).strip().upper()

        # Validate input and retry if invalid (except full column)
        if not is_valid_input(col_input, COLS):
            continue
        col_index = ord(col_input) - ord('A')
        if col_index < 0 or col_index >= COLS:
            continue

        # Try to place checker
        if not place_checker(board, col_index, checker):
            # column full, player loses turn
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Check win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if check_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
