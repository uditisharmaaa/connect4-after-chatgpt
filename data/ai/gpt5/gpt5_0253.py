import os, random, string

# Configurable constants (submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # 2..5
TOKENS = list("XOVHM")[:NUM_PLAYERS]
WIN_LEN = 4

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_and_print(board, col_labels):
    os.system('clear')
    # Header
    print("  " + "   ".join(col_labels))
    line = "+" + "+".join(["---"] * len(col_labels)) + "+"
    print(line)
    for r in range(len(board)):
        row = board[r]
        print("|" + "|".join(f" {c} " for c in row) + "|")
        print(line)

def drop_piece(board, col, token):
    # place from bottom up; return row index if placed else None
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win_from(board, r, c, token):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    rows, cols = len(board), len(board[0])
    for dr, dc in dirs:
        count = 1
        # forward
        rr, cc = r+dr, c+dc
        while in_bounds(rr,cc,rows,cols) and board[rr][cc]==token:
            count += 1; rr += dr; cc += dc
        # backward
        rr, cc = r-dr, c-dc
        while in_bounds(rr,cc,rows,cols) and board[rr][cc]==token:
            count += 1; rr -= dr; cc -= dc
        if count >= WIN_LEN:
            return True
    return False

def board_full(board):
    # If top row has no spaces, board is full
    return all(cell != " " for cell in board[0])

def get_valid_column_input(col_labels):
    while True:
        s = input("Please enter a column: ").strip().upper()
        if len(s) == 1 and s in col_labels:
            return col_labels.index(s)
        print("Invalid input. Enter a single letter within the board.")

def main():
    # Setup
    assert 2 <= NUM_PLAYERS <= 5
    assert 1 <= COLS <= 26
    board = make_board(ROWS, COLS)
    col_labels = list(string.ascii_uppercase[:COLS])
    current = random.randrange(NUM_PLAYERS)

    clear_and_print(board, col_labels)
    print(f"Player {TOKENS[current]}, please enter a column:")

    winner = None
    while True:
        # Get a valid column letter (only letter validation here)
        col = get_valid_column_input(col_labels)
        row = drop_piece(board, col, TOKENS[current])
        if row is None:
            # Column full: lose the turn
            clear_and_print(board, col_labels)
            print(f"Column {col_labels[col]} is full. Player {TOKENS[current]} loses the turn.")
        else:
            # Placed successfully: check win
            if check_win_from(board, row, col, TOKENS[current]):
                clear_and_print(board, col_labels)
                print(f"Player {TOKENS[current]} won!")
                break
            # Check draw
            if board_full(board):
                clear_and_print(board, col_labels)
                print("It's a draw!")
                break
            clear_and_print(board, col_labels)
        # Next player's turn
        current = (current + 1) % NUM_PLAYERS
        print(f"Player {TOKENS[current]}, please enter a column:")

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print()
