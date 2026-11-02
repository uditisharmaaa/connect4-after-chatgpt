import os
import random
import string

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4
COLUMN_LABELS = string.ascii_uppercase[:COLS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    line = "+---" * COLS + "+"
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)


def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    return col_char in COLUMN_LABELS


def column_to_index(col_char):
    return COLUMN_LABELS.index(col_char)


def get_lowest_empty_row(board, col_idx):
    # Start from bottom row and go up
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return -1


def place_checker(board, col_idx, checker):
    row = get_lowest_empty_row(board, col_idx)
    if row == -1:
        return False  # Column full
    board[row][col_idx] = checker
    return True


def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_CONDITION:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_CONDITION:
                    return True
            else:
                count = 0

    # Diagonal check (\ direction)
    for r in range(ROWS - WIN_CONDITION + 1):
        for c in range(COLS - WIN_CONDITION + 1):
            count = 0
            for i in range(WIN_CONDITION):
                if board[r + i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_CONDITION:
                return True

    # Diagonal check (/ direction)
    for r in range(WIN_CONDITION - 1, ROWS):
        for c in range(COLS - WIN_CONDITION + 1):
            count = 0
            for i in range(WIN_CONDITION):
                if board[r - i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_CONDITION:
                return True

    return False


def is_draw(board):
    # Draw if all top cells are occupied (no empty spaces in top row)
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True


def get_player_input(player_checker):
    prompt = f"Player {player_checker}, please enter a column: "
    while True:
        inp = input(prompt).strip().upper()
        if not is_valid_column(inp):
            print(f"Invalid input. Please enter a column letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
            continue
        col_idx = column_to_index(inp)
        # Check if column is full
        if get_lowest_empty_row(board, col_idx) == -1:
            # Player loses turn if column full
            print(f"Column {inp} is full. Turn lost.")
            return None
        return col_idx


# Initialize game
board = create_board(ROWS, COLS)
players = CHECKERS[:NUM_PLAYERS]

# Select random starting player
current_player_idx = random.randint(0, NUM_PLAYERS - 1)

print_board(board)

while True:
    player_checker = players[current_player_idx]
    col = get_player_input(player_checker)
    # If player lost turn, just pass turn on
    if col is not None:
        placed = place_checker(board, col, player_checker)
        # Defensive: placed should be True here because we checked above
        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break
    else:
        # Column full -> turn lost, print board for clarity
        print_board(board)

    # Next player's turn
    current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
