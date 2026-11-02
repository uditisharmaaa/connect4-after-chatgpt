import os
import random

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
VALID_COLUMNS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  " + "   ".join(VALID_COLUMNS)
    print(header)
    # Print horizontal divider
    line = "+---" * COLS + "+"
    for row in range(ROWS):
        print(line)
        row_str = "| " + " | ".join(board[row]) + " |"
        print(row_str)
    print(line)

def valid_column_input(input_str):
    if len(input_str) != 1:
        return False
    if input_str not in VALID_COLUMNS:
        return False
    return True

def is_column_full(board, col_idx):
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    # Start from bottom row, go up, find first empty spot
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r, col_idx
    return None  # Column full; handled outside

def check_direction(board, start_r, start_c, dr, dc, checker):
    count = 0
    r, c = start_r, start_c
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, r, c, checker):
    # Check all directions by counting consecutive checkers including the placed checker
    # horizontal
    left = check_direction(board, r, c, 0, -1, checker) - 1
    right = check_direction(board, r, c, 0, 1, checker)
    if left + right >= WIN_COUNT:
        return True
    # vertical
    up = check_direction(board, r, c, -1, 0, checker) - 1
    down = check_direction(board, r, c, 1, 0, checker)
    if up + down >= WIN_COUNT:
        return True
    # diagonal top-left to bottom-right
    up_left = check_direction(board, r, c, -1, -1, checker) - 1
    down_right = check_direction(board, r, c, 1, 1, checker)
    if up_left + down_right >= WIN_COUNT:
        return True
    # diagonal top-right to bottom-left
    up_right = check_direction(board, r, c, -1, 1, checker) - 1
    down_left = check_direction(board, r, c, 1, -1, checker)
    if up_right + down_left >= WIN_COUNT:
        return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def get_next_player(current_idx, total_players):
    return (current_idx + 1) % total_players

def main():
    total_players = 2  # As per submission requirements
    board = create_board(ROWS, COLS)
    players = PLAYERS[:total_players]
    current_player_idx = random.randint(0, total_players - 1)

    print_board(board)
    while True:
        current_player = players[current_player_idx]
        prompt = f"Player {current_player}, please enter a column: "
        while True:
            user_input = input(prompt).strip().upper()
            if not valid_column_input(user_input):
                # Invalid column input: length, character out of range
                continue
            col_idx = ord(user_input) - ord('A')
            if is_column_full(board, col_idx):
                # Column full: turn is lost
                break
            # Place the checker
            placed_pos = place_checker(board, col_idx, current_player)
            if placed_pos is None:
                # Redundant because we checked column full before, but keep for safety
                break
            # Checker placed successfully, break input loop
            break

        print_board(board)

        # If we placed a checker, check for a win/draw
        if placed_pos:
            r, c = placed_pos
            if check_win(board, r, c, current_player):
                print(f"Player {current_player} won!")
                break

        if board_full(board):
            print("The game is a draw!")
            break

        # If column was full and player lost turn, we skip win check and go to next player anyway
        current_player_idx = get_next_player(current_player_idx, total_players)

if __name__ == "__main__":
    main()
