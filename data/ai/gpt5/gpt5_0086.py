import os
import random

# Constants (adjustable within constraints)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
WIN_LENGTH = 4  # Always 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    labels = []
    for i in range(cols):
        labels.append(chr(ord('A') + i))
    return labels

def print_board(board):
    labels = column_labels(len(board[0]))
    # Top labels line
    label_line = "  " + "   ".join(labels)
    print(label_line)
    # Grid
    horizontal = "+" + ("---+" * len(board[0]))
    for r in range(len(board)):
        print(horizontal)
        row_cells = []
        for c in range(len(board[0])):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(horizontal)

def is_valid_input(user_input, cols):
    if len(user_input) != 1:
        return False
    ch = user_input.upper()
    if not ('A' <= ch <= 'Z'):
        return False
    index = ord(ch) - ord('A')
    return 0 <= index < cols

def get_column_index(user_input):
    return ord(user_input.upper()) - ord('A')

def find_drop_row(board, col):
    # Return the row index where the checker should be placed, or None if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def check_direction(board, start_r, start_c, dr, dc, checker):
    count = 0
    r = start_r
    c = start_c
    rows = len(board)
    cols = len(board[0])
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        if count == WIN_LENGTH:
            return True
        r += dr
        c += dc
    return False

def check_win_for(board, checker):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # Check right
            if c + WIN_LENGTH - 1 < cols and check_direction(board, r, c, 0, 1, checker):
                return True
            # Check down
            if r + WIN_LENGTH - 1 < rows and check_direction(board, r, c, 1, 0, checker):
                return True
            # Check down-right
            if (r + WIN_LENGTH - 1 < rows) and (c + WIN_LENGTH - 1 < cols) and check_direction(board, r, c, 1, 1, checker):
                return True
            # Check down-left
            if (r + WIN_LENGTH - 1 < rows) and (c - (WIN_LENGTH - 1) >= 0) and check_direction(board, r, c, 1, -1, checker):
                return True
    return False

def is_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    # Safety checks for constraints
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        return
    if ROWS < 1:
        print("ROWS must be at least 1.")
        return

    board = create_board(ROWS, COLS)
    players = CHECKERS
    current_player_index = random.randint(0, len(players) - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_index]
        # Prompt and validate input
        labels = column_labels(COLS)
        prompt = f"Player {current_checker}, please enter a column: "
        col_input = input(prompt).strip().upper()
        while not is_valid_input(col_input, COLS):
            print("Invalid input. Please enter a valid uppercase column letter within the board.")
            col_input = input(prompt).strip().upper()

        col = get_column_index(col_input)
        row_to_place = find_drop_row(board, col)

        if row_to_place is None:
            # Column full: turn is invalid and the player loses the turn
            print(f"Column {labels[col]} is full. Turn lost.")
            input("Press Enter to continue...")
            current_player_index = (current_player_index + 1) % len(players)
            continue

        # Place checker
        board[row_to_place][col] = current_checker

        # Check for win
        if check_win_for(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % len(players)

if __name__ == "__main__":
    main()
