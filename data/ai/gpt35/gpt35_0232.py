import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, cols=COLUMNS):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers A, B, C, ...
    header = "  "
    for i in range(len(board[0])):
        header += "  " + chr(ord('A') + i) + " "
    print(header)
    
    horizontal_line = "+" + "---+" * len(board[0])
    for row in board:
        print(horizontal_line)
        print("| " + " | ".join(row) + " |")
    print(horizontal_line)

def is_valid_column(input_col, board):
    if len(input_col) != 1:
        return False
    if not input_col.isalpha():
        return False
    col_index = ord(input_col) - ord('A')
    if col_index < 0 or col_index >= len(board[0]):
        return False
    # Check if column is full
    if board[0][col_index] != " ":
        return False
    return True

def get_next_open_row(board, col):
    # Return the lowest available row index (largest row number) in the column
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            return r
    return None  # Column full

def place_checker(board, col, checker):
    row = get_next_open_row(board, col)
    if row is not None:
        board[row][col] = checker
        return row
    else:
        return None  # Full column

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < len(board) and 0 <= col < len(board[0]):
        if board[row][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        row += delta_row
        col += delta_col
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal for win
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count >= WIN_COUNT:
                    return True
            else:
                count = 0

    # Check vertical for win
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count >= WIN_COUNT:
                    return True
            else:
                count = 0

    # Check diagonals (bottom left to top right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r+i][c+i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    # Check diagonals (top left to bottom right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r-i][c+i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    return False

def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def input_column(player_checker, board):
    while True:
        choice = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(choice, board):
            # Check if input is a valid letter (to differentiate between invalid char and full column)
            if len(choice) == 1 and choice.isalpha():
                col_idx = ord(choice) - ord('A')
                if 0 <= col_idx < len(board[0]) and board[0][col_idx] != " ":
                    # Column full, turn invalid
                    print(f"Column {choice} is full. Turn lost.")
                    return None
            print(f"Invalid input. Please enter a valid column letter (A-{chr(ord('A')+len(board[0])-1)}).")
            continue
        return ord(choice) - ord('A')

def main():
    # Setup game constants for this assignment submission
    rows = ROWS
    cols = COLUMNS
    num_players = 2
    players = PLAYERS[:num_players]

    board = create_board(rows, cols)
    current_player_idx = random.randint(0, num_players -1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        col = input_column(player_checker, board)
        if col is None:
            # Turn lost because column full
            # Switch to next player
            current_player_idx = (current_player_idx + 1) % num_players
            print_board(board)
            continue

        row = place_checker(board, col, player_checker)
        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("The game is a draw.")
            break

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
