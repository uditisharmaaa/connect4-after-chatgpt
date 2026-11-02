import os, random, string

# Config (submission requires ROWS=6, COLS=7, PLAYERS=2)
ROWS, COLS = 6, 7      # up to 26 columns supported
PLAYERS = 2            # between 2 and 5 players
TOKENS = ["X", "O", "V", "H", "M"][:PLAYERS]
WIN_N = 4

def clear(): os.system('clear')

def make_board(r, c): return [[" " for _ in range(c)] for _ in range(r)]

def print_board(board):
    clear()
    cols = len(board[0])
    letters = list(string.ascii_uppercase[:cols])
    print("  " + "   ".join(letters))
    print("+" + ("---+" * cols))
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        print("+" + ("---+" * cols))

def valid_col_input(s, cols):
    if len(s) != 1 or not s.isalpha(): return False
    c = s.upper()
    return "A" <= c <= chr(ord('A') + cols - 1)

def drop_checker(board, col, token):
    # place in lowest empty row; return (row_index) or None if column full
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None

def in_bounds(r, c, rows, cols): return 0 <= r < rows and 0 <= c < cols

def check_win(board, r, c, token):
    # check 4 in a row including position (r,c)
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    rows, cols = len(board), len(board[0])
    for dr, dc in directions:
        count = 1
        for sign in (1, -1):
            nr, nc = r + sign*dr, c + sign*dc
            while in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
                count += 1
                if count >= WIN_N: return True
                nr += sign*dr
                nc += sign*dc
    return False

def board_full(board): return all(cell != " " for row in board for cell in row)

def main():
    board = make_board(ROWS, COLS)
    current = random.randrange(PLAYERS)
    print_board(board)
    while True:
        token = TOKENS[current]
        print(f"Player {token}, please enter a column:")
        col_input = input().strip().upper()
        while not valid_col_input(col_input, COLS):
            print("Invalid input. Enter a valid column letter:")
            col_input = input().strip().upper()
        col = ord(col_input) - ord('A')
        row_placed = drop_checker(board, col, token)
        if row_placed is None:
            print_board(board)
            print(f"Column {col_input} is full. Turn lost.")
            current = (current + 1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, row_placed, col, token):
            print(f"Player {token} won!")
            break
        if board_full(board):
            print("It's a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
