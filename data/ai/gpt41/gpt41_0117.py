import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # Set to 2 for submission (change up to 5)

# Board labels
COL_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(COL_LABELS))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_player_input(board, player):
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in COL_LABELS:
            print("Invalid column. Try again.")
            continue
        col_index = COL_LABELS.index(col_input)
        if board[0][col_index] != " ":
            print("Column is full. You lose your turn.")
            return None
        return col_index

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return board.index(row), col
    return None, None

def board_full(board):
    return all(cell != " " for cell in board[0])

def check_win(board, row, col, checker):
    def count_dir(delta_row, delta_col):
        r, c = row + delta_row, col + delta_col
        count = 0
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col
        return count

    # Directions: horizontal, vertical, diag down = /, diag up = \
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]
    for dr, dc in directions:
        count = 1 + count_dir(dr, dc) + count_dir(-dr, -dc)
        if count >= 4:
            return True
    return False

def main():
    board = create_board(ROWS, COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current]
        col = get_player_input(board, checker)
        if col is not None:
            row, col_index = drop_checker(board, col, checker)
            print_board(board)
            if check_win(board, row, col_index, checker):
                print(f"Player {checker} won!")
                break
            if board_full(board):
                print("Draw!")
                break
        else:
            print("Turn lost due to full column.")
            print_board(board)
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
