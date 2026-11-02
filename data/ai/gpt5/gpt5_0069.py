import os, random, string

# Configuration (submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # up to 26 supported
N_PLAYERS = 2  # 2..5 supported
TOKENS = ['X', 'O', 'V', 'H', 'M'][:N_PLAYERS]
WIN_LEN = 4

def clear():
    os.system('clear')

def create_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(board):
    clear()
    cols = len(board[0])
    letters = list(string.ascii_uppercase[:cols])
    # Header
    print("  " + "   ".join(letters))
    # Rows from top to bottom
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(sep)
        row = board[r]
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
    print(sep)

def valid_col_input(s, cols):
    if not s: return None
    s = s.strip().upper()
    if len(s) != 1: return None
    if s < 'A' or s >= chr(ord('A') + cols): return None
    return ord(s) - ord('A')

def drop_checker(board, col, token):
    # Place from bottom upward
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, token):
    rows, cols = len(board), len(board[0])
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token: continue
            for dr, dc in directions:
                cnt = 1
                nr, nc = r+dr, c+dc
                while cnt < WIN_LEN and in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
                    cnt += 1
                    nr += dr; nc += dc
                if cnt >= WIN_LEN:
                    return True
    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    current = random.randrange(N_PLAYERS)
    print_board(board)
    while True:
        token = TOKENS[current]
        print(f"Player {token}, please enter a column:")
        col = None
        while col is None:
            s = input().strip()
            col = valid_col_input(s, COLS)
            if col is None:
                print("Invalid input. Please enter a valid column letter:")
        row_placed = drop_checker(board, col, token)
        print_board(board)
        if row_placed is None:
            print(f"Column {chr(ord('A')+col)} is full. Turn lost.")
        else:
            if check_win(board, token):
                print(f"Player {token} won!")
                break
            if board_full(board):
                print("Game is a draw.")
                break
        current = (current + 1) % N_PLAYERS

if __name__ == "__main__":
    main()
