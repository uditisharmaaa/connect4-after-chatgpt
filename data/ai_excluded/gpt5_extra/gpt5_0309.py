import os, random, string, sys

# Constants (submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
PLAYERS = 2  # supports 2..5

CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
EMPTY = ' '

def clear():
    os.system('clear')

def make_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    sep = '+' + '---+' * cols
    print(header)
    print(sep)
    for r in range(len(board)):
        row = '|' + '|'.join(f' {board[r][c]} ' for c in range(cols)) + '|'
        print(row)
        print(sep)

def col_from_input(s, cols):
    s = s.strip().upper()
    if len(s) != 1 or s < 'A' or ord(s) - ord('A') >= cols:
        return None
    return ord(s) - ord('A')

def drop_checker(board, col, ch):
    # returns (row_index or None if full)
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = ch
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, r, c):
    # Check 4-in-a-row through (r,c)
    ch = board[r][c]
    if ch == EMPTY: return False
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    rows, cols = len(board), len(board[0])
    for dr, dc in dirs:
        cnt = 1
        for sign in (1, -1):
            nr, nc = r + dr*sign, c + dc*sign
            while in_bounds(nr, nc, rows, cols) and board[nr][nc] == ch:
                cnt += 1
                if cnt >= 4: return True
                nr += dr*sign; nc += dc*sign
    return False

def board_full(board):
    return all(cell != EMPTY for cell in board[0])

def main():
    if COLS > 26 or not (2 <= PLAYERS <= 5):
        print("Invalid configuration."); sys.exit(1)

    board = make_board(ROWS, COLS)
    current = random.randrange(PLAYERS)

    while True:
        clear()
        print_board(board)
        print(f"Player {CHECKERS[current]}, please enter a column:")
        # Read and validate input (reprompt until valid letter within board)
        col = None
        while col is None:
            try:
                user = input().strip()
            except EOFError:
                return
            col = col_from_input(user, COLS)
            if col is None:
                print("Invalid input. Please enter a valid column letter (e.g., A).")
        # Try to drop; if column full, lose turn
        row = drop_checker(board, col, CHECKERS[current])
        if row is None:
            print("Column is full. You lose your turn. Press Enter to continue.")
            try: input()
            except EOFError: pass
            current = (current + 1) % PLAYERS
            continue
        # Check win
        if check_win(board, row, col):
            clear()
            print_board(board)
            print(f"Player {CHECKERS[current]} won!")
            break
        # Check draw
        if board_full(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break
        # Next player
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
