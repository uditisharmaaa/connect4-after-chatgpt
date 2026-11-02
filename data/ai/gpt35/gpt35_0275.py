import os
import random

# Constants - modify for other sizes or players, but submission uses 6 rows, 7 cols, 2 players
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_PLAYERS = 2  # For submission, fixed to 2 players
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]  # Used in order for players 0..NUM_PLAYERS-1

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers A..G (or up to max 26)
    header = "  "
    for c in range(len(board[0])):
        header += f"  {chr(ord('A') + c)} "
    print(header)
    # Print separator line
    line_sep = "+" + "---+" * len(board[0])
    for r in range(len(board)):
        print(line_sep)
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(line_sep)

def column_letter_to_index(letter):
    # Convert uppercase letter A-Z to column index 0-based
    if len(letter) != 1:
        return -1
    letter = letter.upper()
    index = ord(letter) - ord('A')
    if 0 <= index < COLUMNS:
        return index
    return -1

def is_valid_input(inp):
    # Must be single letter, in range, not filled column
    if len(inp) != 1 or not inp.isalpha():
        return False
    col = column_letter_to_index(inp)
    if col == -1:
        return False
    return True

def is_column_full(board, col):
    # If top row at col is occupied, column is full
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place checker in lowest available spot in column col
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # No space

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    r, c = start_row, start_col
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    return count

def check_win(board, row, col, checker):
    # Check all 4 directions for WIN_LENGTH in a row
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    for dr, dc in directions:
        # count continuous checkers to left/up direction
        count_positive = check_direction(board, row, col, dr, dc, checker) 
        # count continuous checkers in the opposite direction (avoid counting current pos twice, so -1)
        count_negative = check_direction(board, row, col, -dr, -dc, checker) - 1
        if count_positive + count_negative >= WIN_LENGTH:
            return True
    return False

def check_draw(board):
    # If top row has no empty spaces, board is full for sure
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    # Initialize board and players
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    # Random starting player index
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current_player]
        input_prompt = f"Player {checker}, please enter a column: "
        # Get valid input from player
        while True:
            player_input = input(input_prompt).strip().upper()
            if not is_valid_input(player_input):
                print(f"Invalid input '{player_input}'. Please enter a valid column letter A-{chr(ord('A') + COLUMNS - 1)}.")
                continue
            col = column_letter_to_index(player_input)
            if is_column_full(board, col):
                print(f"Column {player_input} is full. You lose your turn.")
                col = -1
            break

        if col != -1:
            row = place_checker(board, col, checker)
            print_board(board)
            # Check win
            if check_win(board, row, col, checker):
                print(f"Player {checker} won!")
                break

            # Check draw
            if check_draw(board):
                print("The game is a draw.")
                break
        else:
            # column full, turn lost, but board still printed to show unchanged board
            print_board(board)

        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
