import os, random, string

# Constants (submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # 2..5

SYMS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
LETTERS = list(string.ascii_uppercase[:COLS])

def clear():
    os.system('clear')

def new_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear()
    cols = len(board[0])
    # Header
    print("  " + "   ".join(LETTERS[:cols]))
    print("+---" * cols + "+")
    for r in range(len(board)):
        row = board[r]
        print("| " + " | ".join(row) + " |")
        print("+---" * cols + "+")

def get_column_input(prompt):
    while True:
        s = input(prompt).strip().upper()
        if len(s) == 1 and s in LETTERS[:COLS]:
            return LETTERS.index(s)
        # keep asking until valid input (does not lose turn)

def drop_checker(board, col, sym):
    # returns (row_index) if placed, or None if column full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, r, c, sym):
    # directions: (dr, dc) pairs; count both ways
    for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
        count = 1
        for s in (1, -1):
            rr, cc = r + s*dr, c + s*dc
            while in_bounds(rr, cc) and board[rr][cc] == sym:
                count += 1
                if count >= 4:
                    return True
                rr += s*dr
                cc += s*dc
        if count >= 4:
            return True
    return False

def board_full(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    assert 2 <= NUM_PLAYERS <= 5 and 1 <= COLS <= 26
    board = new_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    print_board(board)

    while True:
        sym = SYMS[current]
        col = get_column_input(f"Player {sym}, please enter a column: ")
        row = drop_checker(board, col, sym)
        if row is None:
            # Column full: invalid turn and player loses the turn
            print_board(board)
            current = (current + 1) % NUM_PLAYERS
            continue
        # After a valid placement, update display
        print_board(board)
        if check_win(board, row, col, sym):
            print(f"Player {sym} won!")
            break
        if board_full(board):
            print("Draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
