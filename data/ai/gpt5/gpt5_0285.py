import os, random, sys

# Configuration (submission requires these defaults)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
LETTERS = [chr(ord('A') + i) for i in range(min(COLS, 26))]

def clear():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear()
    cols = len(board[0])
    header = "  " + "   ".join(LETTERS[:cols])
    sep = "+" + ("---+" * cols)
    print(header)
    for r in range(len(board)):
        print(sep)
        row = "|"
        for c in range(cols):
            row += f" {board[r][c]} |"
        print(row)
    print(sep)

def get_column_input(player_checker):
    while True:
        try:
            s = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        except EOFError:
            sys.exit(0)
        if len(s) != 1 or not s.isalpha():
            continue
        if s not in LETTERS[:COLS]:
            continue
        return LETTERS.index(s)

def drop_checker(board, col, checker):
    # place in lowest empty row (from bottom)
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None  # column full

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, last_r, last_c, checker):
    if last_r is None:
        return False
    rows, cols = len(board), len(board[0])
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1
        for sign in (1, -1):
            r, c = last_r, last_c
            while True:
                r += dr * sign
                c += dc * sign
                if in_bounds(r, c, rows, cols) and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    if COLS > 26 or NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Invalid configuration.")
        return
    board = create_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    print_board(board)
    last_move = (None, None, None)  # r, c, checker
    while True:
        checker = CHECKERS[current]
        col = get_column_input(checker)
        placed = drop_checker(board, col, checker)
        if placed is None:
            # Column full: lose turn
            print_board(board)
            print(f"Column {LETTERS[col]} is full. Player {checker} loses the turn.")
            current = (current + 1) % NUM_PLAYERS
            continue
        r, c = placed
        print_board(board)
        last_move = (r, c, checker)
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
