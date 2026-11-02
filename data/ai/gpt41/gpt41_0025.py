import os
import random

# ----------- Constants -----------
ROWS = 6
COLS = 7
MAX_COLS = 26
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY = " "

# ----------- Board Functions -----------
def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([EMPTY] * cols)
    return board

def print_board(board, col_labels):
    os.system('clear')
    # column labels
    label_row = "  " + "   ".join(col_labels)
    print(label_row)
    print("+" + "---+" * len(col_labels))
    for r in range(len(board)):
        row = "|"
        for c in range(len(board[0])):
            row += " {} |".format(board[r][c])
        print(row)
        print("+" + "---+" * len(col_labels))

# ----------- Gameplay Functions -----------
def get_valid_columns(board):
    cols = []
    for c in range(len(board[0])):
        if board[0][c] == EMPTY:
            cols.append(c)
    return cols

def input_column(board, col_labels, player_char):
    while True:
        col_input = input(f"Player {player_char}, please enter a column: ").upper()
        if len(col_input) != 1 or col_input not in col_labels:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_idx = col_labels.index(col_input)
        if board[0][col_idx] != EMPTY:
            print("Column is full! You lose this turn.")
            return None
        else:
            return col_idx

def place_checker(board, col, checker):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = checker
            return row, col
    return None

def is_full(board):
    for c in range(len(board[0])):
        if board[0][c] == EMPTY:
            return False
    return True

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    # Vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    # Diagonal (up-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

# ----------- Main Game Loop -----------
def main():
    # Check dimensions and players
    if COLS > MAX_COLS or NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Invalid board size or number of players")
        return

    board = create_board(ROWS, COLS)
    col_labels = [chr(ord('A') + i) for i in range(COLS)]
    player_checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board, col_labels)
    print(f"Player {player_checkers[current_player]} starts!")

    while True:
        print_board(board, col_labels)
        valid_cols = get_valid_columns(board)
        # If the column chosen is full, player loses turn!
        col = input_column(board, col_labels, player_checkers[current_player])
        if col is None:
            # Lose turn
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        row, col = place_checker(board, col, player_checkers[current_player])
        print_board(board, col_labels)
        if check_win(board, player_checkers[current_player]):
            print(f"Player {player_checkers[current_player]} won!")
            break
        elif is_full(board):
            print("It's a draw!")
            break
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
