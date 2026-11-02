import os, random, sys

# Constants (submission: 6x7 board, 2 players)
ROWS, COLS = 6, 7
MAX_COLS = 26
PLAYERS_ALL = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # between 2 and 5

assert 2 <= NUM_PLAYERS <= 5 and 1 <= COLS <= MAX_COLS

PLAYERS = PLAYERS_ALL[:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear_and_print(board):
    os.system('clear')
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * len(board[0])) + "+"
    for row in board:
        print(sep)
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
    print(sep)

def valid_col_input(s, cols):
    if len(s) != 1 or not s.isalpha():
        return False
    idx = ord(s.upper()) - ord('A')
    return 0 <= idx < cols

def get_col_input(player, cols):
    while True:
        try:
            s = input(f"Player {player}, please enter a column: ").strip()
        except EOFError:
            sys.exit(0)
        if valid_col_input(s, cols):
            return ord(s.upper()) - ord('A')
        # keep asking until valid per spec

def drop_checker(board, col, sym):
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return r, col
    return None  # column full, turn lost

def check_winner(board):
    R, C = len(board), len(board[0])
    dirs = [(0,1),(1,0),(1,1),(-1,1)]
    for r in range(R):
        for c in range(C):
            ch = board[r][c]
            if ch == " ":
                continue
            for dr, dc in dirs:
                rr, cc = r, c
                ok = True
                for _ in range(3):
                    rr += dr; cc += dc
                    if not (0 <= rr < R and 0 <= cc < C and board[rr][cc] == ch):
                        ok = False; break
                if ok:
                    return ch
    return None

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = make_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    clear_and_print(board)
    while True:
        player = PLAYERS[current]
        col = get_col_input(player, COLS)
        placed = drop_checker(board, col, player)
        clear_and_print(board)
        if placed is None:
            # Column full: turn lost
            pass
        else:
            winner = check_winner(board)
            if winner:
                print(f"Player {winner} won!")
                break
            if is_draw(board):
                print("It's a draw!")
                break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
