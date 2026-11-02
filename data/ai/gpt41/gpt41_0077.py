import os
import random
import string

# ======= CONSTANTS =======
ROWS = 6
COLUMNS = 7   # max 26
PLAYERS = 2   # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLUMNS])

# ======= FUNCTIONS =======

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    print("  ", end="")
    for label in COLUMN_LABELS:
        print(f" {label}  ", end="")
    print()
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "---+" * COLUMNS)

def input_column():
    while True:
        col = input().strip().upper()
        if len(col) != 1 or col not in COLUMN_LABELS:
            print("Invalid column. Please enter a valid column letter:")
        else:
            return COLUMN_LABELS.index(col)

def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return None  # Column full

def check_win(board, row, col, checker):
    # Directions: (dr, dc)
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row+dr, col+dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row-dr, col-dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != " " for cell in board[0])

# ======= MAIN LOOP =======

def main():
    board = create_board(ROWS, COLUMNS)
    player_indices = list(range(PLAYERS))
    current = random.choice(player_indices)
    print_board(board)
    print(f"Player {CHECKERS[current]}, please enter a column:")
    while True:
        col = input_column()
        row = place_checker(board, col, CHECKERS[current])
        if row is None:
            print("Column full! You lost your turn.")
        else:
            print_board(board)
            if check_win(board, row, col, CHECKERS[current]):
                print(f"Player {CHECKERS[current]} won!")
                break
            if is_draw(board):
                print("Game is a draw!")
                break
        current = (current + 1) % PLAYERS
        if row is not None:
            print(f"Player {CHECKERS[current]}, please enter a column:")
        else:
            print(f"Player {CHECKERS[current]}, please enter a column (previous player lost turn):")

if __name__ == "__main__":
    main()
