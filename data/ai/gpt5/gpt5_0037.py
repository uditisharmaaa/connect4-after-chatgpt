import os
import random
import string

# Constants (you may change these for testing; submission should be 6x7 with 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    letters = string.ascii_uppercase[:cols]
    # Header
    header = "  " + "   ".join(letters)
    print(header)
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(sep)
        row = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row)
    print(sep)

def col_from_input(s, cols):
    if len(s) != 1 or s not in string.ascii_uppercase[:cols]:
        return None
    return ord(s) - ord('A')

def drop_checker(board, col, token):
    # returns (row, col) placed or None if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return (r, col)
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win_from(board, r, c, token):
    rows, cols = len(board), len(board[0])
    for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
        count = 1
        # forward
        nr, nc = r + dr, c + dc
        while in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
            count += 1
            nr += dr
            nc += dc
        # backward
        nr, nc = r - dr, c - dc
        while in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
            count += 1
            nr -= dr
            nc -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    if not (2 <= NUM_PLAYERS <= 5): 
        raise ValueError("NUM_PLAYERS must be between 2 and 5")
    if not (1 <= COLS <= 26):
        raise ValueError("COLS must be between 1 and 26")
    board = create_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    while True:
        print_board(board)
        print(f"Player {TOKENS[current]}, please enter a column:")
        # Input validation loop (invalid input does not lose turn)
        col = None
        while col is None:
            try:
                s = input().strip().upper()
            except EOFError:
                return
            col = col_from_input(s, COLS)
            if col is None:
                print("Invalid input. Please enter a valid column letter:")
        # Try to drop; if column full, turn is lost
        pos = drop_checker(board, col, TOKENS[current])
        if pos is None:
            print_board(board)
            print(f"Column {string.ascii_uppercase[col]} is full. Turn lost.")
            current = (current + 1) % NUM_PLAYERS
            continue
        r, c = pos
        # Check win
        if check_win_from(board, r, c, TOKENS[current]):
            print_board(board)
            print(f"Player {TOKENS[current]} won!")
            break
        # Check draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        # Next player
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
