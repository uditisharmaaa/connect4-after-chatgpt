import os
import random
import sys

# Constants
ROWS = 6
COLS = 7
WIN_CONDITION = 4
NUM_PLAYERS = 2  # set to 2 for submission
CHECKERS = ["X", "O", "V", "H", "M"]  # players' checkers in order, max 5 players
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    row_sep = "+" + "---+" * COLS
    for row in range(ROWS):
        print(row_sep)
        row_str = "|"
        for col in range(COLS):
            row_str += f" {board[row][col]} |"
        print(row_str)
    print(row_sep)

def choose_starting_player(num_players):
    return random.randint(0, num_players -1)

def input_column(player_char):
    prompt = f"Player {player_char}, please enter a column: "
    while True:
        col_input = input(prompt).strip().upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter exactly one letter corresponding to a column.")
            continue
        if col_input not in COLUMN_LABELS:
            print("Invalid column. Please enter a valid column letter.")
            continue
        return col_input

def get_column_index(col_letter):
    return ord(col_letter) - ord('A')

def place_checker(board, col_idx, checker):
    # Start from bottom row and find first empty slot
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    return None  # column full

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    r, c = start_row, start_col
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    return count

def check_win(board, row, col, checker):
    # Check all 4 directions for 4 in a row:
    # Horizontal: delta_row=0, delta_col=1
    # Vertical: delta_row=1, delta_col=0
    # Diagonal1 (down-right / up-left): delta_row=1, delta_col=1
    # Diagonal2 (down-left / up-right): delta_row=1, delta_col=-1

    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]

    for dr, dc in directions:
        # count cells to positive direction (excluding start cell)
        pos_count = check_direction(board, row + dr, col + dc, dr, dc, checker)
        # count cells to negative direction (excluding start cell)
        neg_count = check_direction(board, row - dr, col - dc, -dr, -dc, checker)
        total = 1 + pos_count + neg_count
        if total >= WIN_CONDITION:
            return True
    return False

def board_full(board):
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Choose random starting player
    current_player_idx = choose_starting_player(NUM_PLAYERS)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        col_letter = input_column(current_checker)
        col_idx = get_column_index(col_letter)
        pos = place_checker(board, col_idx, current_checker)
        if pos is None:
            # column full -> player loses turn, print board and switch
            print(f"Column {col_letter} is full. Player {current_checker} loses this turn.")
            print_board(board)
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue
        else:
            print_board(board)
            row_placed, col_placed = pos

            # Check for win
            if check_win(board, row_placed, col_placed, current_checker):
                print(f"Player {current_checker} won!")
                sys.exit()

            # Check for draw
            if board_full(board):
                print("The game is a draw!")
                sys.exit()

            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
