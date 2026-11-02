import os
import random
import string

# Constants (you can change these for testing, but submission should be 6x7 and 2 players)
ROWS = 6
COLS = 7       # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Checker symbols in order
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    # Labels A, B, C, ... up to cols (max 26)
    letters = list(string.ascii_uppercase[:cols])
    return letters

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])
    labels = column_labels(cols)

    # Header with column letters
    header = "  " + "   ".join(labels)
    print(header)
    # Top border
    print("+" + "---+" * cols)
    # Board rows
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + "---+" * cols)

def is_valid_column_input(inp, cols):
    if len(inp) != 1:
        return False
    if inp not in column_labels(cols):
        return False
    return True

def get_lowest_empty_row(board, col):
    # Return the row index (from top=0) of the lowest empty cell in column col, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def drop_checker(board, col, checker):
    # Place checker in the lowest empty row of the given column.
    # Return (row, col) if placed, otherwise None if column full.
    row = get_lowest_empty_row(board, col)
    if row is None:
        return None
    board[row][col] = checker
    return (row, col)

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Directions: right, down, down-right, down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while in_bounds(rr, cc, rows, cols) and board[rr][cc] == checker:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False

def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    # Clamp/check constraints
    cols = max(1, min(COLS, 26))
    rows = max(1, ROWS)
    players = max(2, min(NUM_PLAYERS, 5))
    player_checkers = CHECKERS[:players]

    board = create_board(rows, cols)

    # Randomly select starting player
    current_player_index = random.randrange(players)

    # Initial board print
    print_board(board)

    # Game loop
    while True:
        current_checker = player_checkers[current_player_index]
        # Prompt user
        prompt = f"Player {current_checker}, please enter a column: "
        user_inp = input(prompt).strip().upper()

        # Validate input
        while not is_valid_column_input(user_inp, cols):
            print_board(board)
            print("Invalid input. Please enter a valid column letter.")
            user_inp = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        # Convert letter to column index
        col_index = column_labels(cols).index(user_inp)

        # Attempt to drop checker
        placed = drop_checker(board, col_index, current_checker)
        if placed is None:
            # Column full, lose the turn
            print_board(board)
            print("Column is full. Turn lost.")
            # Check for win/draw even though board unchanged (not necessary, but per spec after turn)
            if check_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if board_full(board):
                print("It's a draw!")
                break
            # Next player
            current_player_index = (current_player_index + 1) % players
            continue

        # After a valid move, print board
        print_board(board)

        # Check for win
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player
        current_player_index = (current_player_index + 1) % players

if __name__ == "__main__":
    main()
