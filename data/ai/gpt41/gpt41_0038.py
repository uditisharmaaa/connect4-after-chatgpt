import os
import random

# Constants
NUM_ROWS = 6          # Board Rows
NUM_COLS = 7          # Board Columns (Max 26)
NUM_PLAYERS = 2       # Number of Players (from 2 to 5)

CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
EMPTY = " "

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    # Return list of column indices that are not full
    valid = []
    for col in range(len(board[0])):
        if board[0][col] == EMPTY:
            valid.append(col)
    return valid

def get_column_from_input(inp, cols):
    if len(inp) != 1:
        return None
    inp = inp.upper()
    idx = ord(inp) - ord('A')
    if idx >= 0 and idx < cols:
        return idx
    return None

def is_column_full(board, col):
    return board[0][col] != EMPTY

def place_checker(board, col, checker):
    # Place checker in lowest empty space
    for row in reversed(range(len(board))):
        if board[row][col] == EMPTY:
            board[row][col] = checker
            return row
    return None

def check_line(lst, checker):
    count = 0
    for cell in lst:
        if cell == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def check_victory(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    if check_line(board[row], checker):
        return True

    # Vertical
    col_cells = [board[r][col] for r in range(rows)]
    if check_line(col_cells, checker):
        return True

    # Diagonal (\)
    diag = []
    r, c = row, col
    while r > 0 and c > 0:
        r -= 1
        c -= 1
    while r < rows and c < cols:
        diag.append(board[r][c])
        r += 1
        c += 1
    if check_line(diag, checker):
        return True

    # Diagonal (/)
    diag = []
    r, c = row, col
    while r > 0 and c < cols - 1:
        r -= 1
        c += 1
    while r < rows and c >= 0:
        diag.append(board[r][c])
        r += 1
        c -= 1
    if check_line(diag, checker):
        return True

    return False

def is_draw(board):
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    player_order = list(range(NUM_PLAYERS))
    random.shuffle(player_order)
    current_player_idx = 0

    clear_screen()
    print_board(board)
    print()
    current_player = player_order[current_player_idx]
    print("Player {} will start!".format(CHECKERS[current_player]))

    while True:
        current_player = player_order[current_player_idx]
        checker = CHECKERS[current_player]

        valid_columns = get_valid_columns(board)

        print()
        col_letter = input("Player {}, please enter a column: ".format(checker)).strip().upper()
        col = get_column_from_input(col_letter, NUM_COLS)

        if col is None or col not in range(NUM_COLS):
            print("Invalid column. Please enter a column letter from A to {}.".format(chr(ord('A') + NUM_COLS - 1)))
            continue

        if is_column_full(board, col):
            print("Column is full. You lose your turn.")
            # Lose the turn, do not ask again for this player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        row = place_checker(board, col, checker)

        clear_screen()
        print_board(board)

        if check_victory(board, row, col, checker):
            print("Player {} won!".format(checker))
            break

        if is_draw(board):
            print("Draw! No one wins.")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
