import os
import random
import string

# Constants (submission must be 6x7 board and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # supports 2..5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    letters = string.ascii_uppercase[:cols]
    # Header
    print('  ' + '   '.join(letters))
    # Rows
    sep = '+' + '---+' * cols
    for r in range(len(board)):
        print(sep)
        row_str = '|' + '|'.join(f' {board[r][c]} ' for c in range(cols)) + '|'
        print(row_str)
    print(sep)

def col_from_input(s, cols):
    if not s or len(s.strip()) != 1:
        return None
    ch = s.strip().upper()
    if ch < 'A' or ch >= chr(ord('A') + cols):
        return None
    return ord(ch) - ord('A')

def drop_checker(board, col, symbol):
    # place in lowest available row; return row index or None if full
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, r, c, sym):
    # count consecutive in 4 directions
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    rows, cols = len(board), len(board[0])
    for dr, dc in dirs:
        cnt = 1
        for sign in (1, -1):
            nr, nc = r + sign*dr, c + sign*dc
            while in_bounds(nr, nc, rows, cols) and board[nr][nc] == sym:
                cnt += 1
                nr += sign*dr
                nc += sign*dc
        if cnt >= 4:
            return True
    return False

def board_full(board):
    return all(board[0][c] != ' ' for c in range(len(board[0])))

def main():
    rows, cols = ROWS, COLS
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    board = create_board(rows, cols)
    current = random.randrange(len(players))

    clear()
    print_board(board)

    while True:
        player = players[current]
        inp = input(f"Player {player}, please enter a column: ")
        col = col_from_input(inp, cols)
        while col is None:
            inp = input("Invalid input. Please enter a valid column letter: ")
            col = col_from_input(inp, cols)

        row = drop_checker(board, col, player)
        clear()
        print_board(board)

        if row is None:
            # column full: lose turn
            current = (current + 1) % len(players)
        else:
            if check_win(board, row, col, player):
                print(f"Player {player} won!")
                break
            if board_full(board):
                print("It's a draw!")
                break
            current = (current + 1) % len(players)

if __name__ == "__main__":
    main()
