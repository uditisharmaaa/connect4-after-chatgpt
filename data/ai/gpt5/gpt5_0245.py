import os, random, string, sys

# Constants (submission must be 6x7 with 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear():
    os.system('clear')

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    line = "+" + "+".join(["---"] * cols) + "+"
    print(header)
    print(line)
    for r in range(len(board)):
        row = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row)
        print(line)

def valid_col_input(s, cols):
    return len(s) == 1 and 'A' <= s <= chr(ord('A') + cols - 1)

def drop_checker(board, col, checker):
    # returns row index where placed, or None if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, r, c, checker):
    rows, cols = len(board), len(board[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in dirs:
        cnt = 1
        for sign in (1, -1):
            nr, nc = r + dr*sign, c + dc*sign
            while in_bounds(nr, nc, rows, cols) and board[nr][nc] == checker:
                cnt += 1
                if cnt >= 4: return True
                nr += dr*sign
                nc += dc*sign
    return False

def board_full(board):
    return all(cell != " " for cell in board[0])  # top row filled means full columns; also implies full board due to gravity

def main():
    if not (2 <= NUM_PLAYERS <= 5) or not (1 <= COLS <= 26):
        print("Invalid configuration"); sys.exit(1)
    board = make_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    while True:
        clear()
        print_board(board)
        checker = CHECKERS[current]
        # Prompt and validate input; re-prompt on invalid input only
        col = None
        while True:
            inp = input(f"Player {checker}, please enter a column: ").strip().upper()
            if valid_col_input(inp, COLS):
                col = ord(inp) - ord('A')
                break
        # Attempt to drop; if column full, lose turn
        row = drop_checker(board, col, checker)
        if row is None:
            current = (current + 1) % NUM_PLAYERS
            continue
        # Check win
        if check_win(board, row, col, checker):
            clear()
            print_board(board)
            print(f"Player {checker} won!")
            break
        # Check draw
        if board_full(board):
            clear()
            print_board(board)
            print("Game is a draw.")
            break
        # Next player
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
