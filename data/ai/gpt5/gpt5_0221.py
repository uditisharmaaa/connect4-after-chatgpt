import os, random, string

# Constants (submission requires 6x7 and 2 players)
ROWS, COLS = 6, 7              # up to 26 columns
NUM_PLAYERS = 2                # between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
WIN_LEN = 4

def create_board(r, c):
    return [[' ' for _ in range(c)] for _ in range(r)]

def clear_and_print(board, players, current_idx):
    os.system('clear')
    letters = string.ascii_uppercase[:len(board[0])]
    print('  ' + '   '.join(letters))
    sep = '+' + '+'.join(['---'] * len(board[0])) + '+'
    for r in range(len(board)):
        print(sep)
        row = '|' + '|'.join(f' {board[r][c]} ' for c in range(len(board[0]))) + '|'
        print(row)
    print(sep)
    print(f"Player {players[current_idx]}, please enter a column:")

def get_valid_column_input(cols):
    letters = string.ascii_uppercase[:cols]
    while True:
        s = input().strip()
        if len(s) == 1 and s in letters:
            return letters.index(s)
        print("Invalid input. Please enter a valid column letter:")

def drop_checker(board, col, ch):
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = ch
            return r
    return None  # column full

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(board, ch):
    R, C = len(board), len(board[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(R):
        for c in range(C):
            if board[r][c] != ch:
                continue
            for dr, dc in dirs:
                cnt, rr, cc = 1, r, c
                for _ in range(WIN_LEN-1):
                    rr += dr; cc += dc
                    if in_bounds(rr, cc, R, C) and board[rr][cc] == ch:
                        cnt += 1
                    else:
                        break
                if cnt >= WIN_LEN:
                    return True
    return False

def board_full(board):
    return all(board[0][c] != ' ' for c in range(len(board[0])))

def main():
    if COLS > 26 or NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Configuration error."); return
    board = create_board(ROWS, COLS)
    players = CHECKERS
    current = random.randrange(len(players))
    # Show initial empty board before first move
    clear_and_print(board, players, current)
    while True:
        col = get_valid_column_input(COLS)
        row_idx = drop_checker(board, col, players[current])
        if row_idx is None:
            # Column full: lose turn
            clear_and_print(board, players, (current+1) % len(players))
            print("Column full. Turn lost.")
            current = (current + 1) % len(players)
        else:
            if check_win(board, players[current]):
                clear_and_print(board, players, current)
                print(f"Player {players[current]} won!")
                return
            if board_full(board):
                clear_and_print(board, players, current)
                print("It's a draw!")
                return
            current = (current + 1) % len(players)
            clear_and_print(board, players, current)

if __name__ == "__main__":
    main()
