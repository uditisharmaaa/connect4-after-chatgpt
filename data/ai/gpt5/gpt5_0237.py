import os, random, string

# Constants (submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # 2 to 5
TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    letters = string.ascii_uppercase[:cols]
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(sep)
        print("|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|")
    print(sep)

def drop_checker(board, col, token):
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
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                cnt = 1
                nr, nc = r + dr, c + dc
                while cnt < 4 and in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
                    cnt += 1
                    nr += dr
                    nc += dc
                if cnt == 4:
                    return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_valid_column(cols):
    letters = string.ascii_uppercase[:cols]
    while True:
        s = input().strip().upper()
        if len(s) == 1 and s in letters:
            return ord(s) - ord('A')
        print("Invalid input. Please enter a valid column letter:")

def main():
    if not (2 <= NUM_PLAYERS <= 5): raise SystemExit("NUM_PLAYERS must be 2..5")
    if not (1 <= COLS <= 26): raise SystemExit("COLS must be 1..26")
    board = create_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    while True:
        clear()
        print_board(board)
        token = TOKENS[current]
        print(f"Player {token}, please enter a column:")
        col = get_valid_column(COLS)
        row = drop_checker(board, col, token)
        # After the turn (even if column full), check win/draw and proceed
        if row is not None and check_win(board, token):
            clear()
            print_board(board)
            print(f"Player {token} won!")
            break
        if check_draw(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
