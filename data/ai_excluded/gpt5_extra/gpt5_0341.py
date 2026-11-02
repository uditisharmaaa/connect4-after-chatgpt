import os, random, string, sys

# Constants (adjustable, but submission uses these)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # 2..5
WIN_LEN = 4
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear():
    os.system('clear')

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(board):
    letters = string.ascii_uppercase[:len(board[0])]
    header = "  " + "   ".join(letters)
    sep = "+" + "+".join(["---"] * len(board[0])) + "+"
    print(header)
    for r in range(len(board)):
        print(sep)
        row = "|" + "|".join(f" {board[r][c]} " for c in range(len(board[0]))) + "|"
        print(row)
    print(sep)

def get_column_input(valid_cols, player_checker):
    while True:
        try:
            s = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        except EOFError:
            sys.exit(0)
        if len(s) == 1 and s.isalpha():
            idx = ord(s) - ord('A')
            if 0 <= idx < valid_cols:
                return idx
        print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, col, checker):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None  # column full

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(board, last_r, last_c, checker):
    if last_r is None: 
        return False
    R, C = len(board), len(board[0])
    dirs = [(0,1),(1,0),(1,1),(-1,1)]
    for dr, dc in dirs:
        count = 1
        for sgn in (1, -1):
            r, c = last_r + sgn*dr, last_c + sgn*dc
            while in_bounds(r, c, R, C) and board[r][c] == checker:
                count += 1
                if count >= WIN_LEN:
                    return True
                r += sgn*dr
                c += sgn*dc
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    assert 2 <= NUM_PLAYERS <= 5 and 1 <= COLS <= 26
    board = make_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    last_move = (None, None, None)  # r, c, checker

    clear()
    print_board(board)

    while True:
        player_checker = CHECKERS[current]
        col = get_column_input(COLS, player_checker)
        move = drop_checker(board, col, player_checker)
        clear()
        print_board(board)

        if move is None:
            print(f"Column {string.ascii_uppercase[col]} is full. Player {player_checker} loses the turn.")
        else:
            r, c = move
            last_move = (r, c, player_checker)
            if check_win(board, r, c, player_checker):
                print(f"Player {player_checker} won!")
                break
            if board_full(board):
                print("It's a draw!")
                break

        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
