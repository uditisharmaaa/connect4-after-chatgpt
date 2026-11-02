import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
MAX_COLUMNS = 26

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column headers
    headers = "  " + "   ".join([chr(ord('A') + i) for i in range(columns)])
    print(headers)
    # Print the board with separators
    row_sep = "+" + "---+" * columns
    for row in board:
        print(row_sep)
        print("| " + " | ".join(row) + " |")
    print(row_sep)

def get_column_index(column_letter):
    column_letter = column_letter.upper()
    idx = ord(column_letter) - ord('A')
    if 0 <= idx < COLUMNS:
        return idx
    return -1

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    """
    Places the checker in the lowest empty space in column col.
    Returns True if placed, False if column full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # horizontal check
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # vertical check
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # diagonal down-right check
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # diagonal down-left check
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(WIN_LENGTH - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def check_draw(board):
    # If any top cell is empty, not draw
    return all(board[0][col] != " " for col in range(len(board[0])))

def get_valid_input(board, current_checker):
    while True:
        prompt = f"Player {current_checker}, please enter a column: "
        user_input = input(prompt).strip().upper()
        if len(user_input) != 1 or not ('A' <= user_input <= chr(ord('A') + COLUMNS - 1)):
            continue
        col = get_column_index(user_input)
        if col == -1:
            continue
        if is_column_full(board, col):
            # Column full -> player loses turn
            return -1
        return col

def main():
    # Validate constants (not required but good practice)
    assert 2 <= PLAYERS <= 5
    assert 1 <= ROWS
    assert 1 <= COLUMNS <= MAX_COLUMNS

    board = create_board(ROWS, COLUMNS)
    player_checkers = CHECKERS[:PLAYERS]

    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        checker = player_checkers[current_player]

        col = get_valid_input(board, checker)

        if col == -1:
            # Column full: player loses turn as per instructions, no placement
            current_player = (current_player + 1) % PLAYERS
            continue

        placed = place_checker(board, col, checker)

        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
