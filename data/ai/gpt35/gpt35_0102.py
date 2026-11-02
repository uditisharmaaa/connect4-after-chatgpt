import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # up to 5 players
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers A-G
    header = "  "
    for c in range(COLS):
        header += "  " + chr(ord('A') + c) + " "
    print(header)
    # Print the board with +---+ lines
    line = "+---" * COLS + "+"
    for r in range(ROWS):
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    return 'A' <= col_char <= chr(ord('A') + COLS - 1)

def get_column_index(col_char):
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col, checker):
    # Place checker in the lowest available row in column col (0-based)
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full
    return None

def check_line(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    for _ in range(WIN_LENGTH):
        # Check boundaries
        if 0 <= row < ROWS and 0 <= col < COLS:
            if board[row][col] == checker:
                count += 1
            else:
                break
        else:
            break
        row += delta_row
        col += delta_col
    return count == WIN_LENGTH

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                # Check horizontally to the right
                if check_line(board, r, c, 0, 1, checker):
                    return True
                # Check vertically downwards
                if check_line(board, r, c, 1, 0, checker):
                    return True
                # Check diagonal down-right
                if check_line(board, r, c, 1, 1, checker):
                    return True
                # Check diagonal down-left
                if check_line(board, r, c, 1, -1, checker):
                    return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    player_checkers = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = player_checkers[current_player_index]
        print(f"Player {checker}, please enter a column:")

        user_input = input().strip().upper()

        # Validate input character is a valid column letter
        if not is_valid_column(user_input):
            print("Invalid input. Please enter a valid column letter.")
            continue

        col = get_column_index(user_input)
        placed = place_checker(board, col, checker)
        if placed is None:
            # Column full - player loses turn
            print(f"Column {user_input} is full. Turn lost.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue
        else:
            print_board(board)
            # Check for win
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            # Check for draw
            if board_full(board):
                print("The game is a draw!")
                break
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
