import os, random, string

# Config (can be changed for testing; submission requires ROWS=6, COLS=7, PLAYERS=2)
ROWS, COLS = 6, 7
PLAYERS = 2  # between 2 and 5
TOKENS = ["X", "O", "V", "H", "M"][:PLAYERS]
assert 2 <= PLAYERS <= 5 and 1 <= ROWS and 1 <= COLS <= 26

def clear():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    headers = "  " + "   ".join(string.ascii_uppercase[:COLS])
    sep = "+" + "---+" * COLS
    print(headers)
    for r in range(ROWS):
        print(sep)
        row = "|" + "|".join(f" {board[r][c]} " for c in range(COLS)) + "|"
        print(row)
    print(sep)

def lowest_empty_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def drop_checker(board, col, token):
    r = lowest_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = token
    return r

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, token):
    dirs = [(1,0),(0,1),(1,1),(1,-1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token:
                continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r + dr, c + dc
                while cnt < 4 and in_bounds(rr, cc) and board[rr][cc] == token:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt == 4:
                    return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def get_valid_column_input():
    valid_letters = set(string.ascii_uppercase[:COLS])
    while True:
        s = input().strip().upper()
        if len(s) == 1 and s in valid_letters:
            return ord(s) - ord('A')
        print("Invalid input. Please enter a column letter:", end=" ")

def main():
    board = create_board()
    current = random.randrange(PLAYERS)
    clear()
    print_board(board)
    while True:
        token = TOKENS[current]
        print(f"Player {token}, please enter a column:", end=" ")
        col = get_valid_column_input()
        row = drop_checker(board, col, token)
        if row is None:
            # Column full: lose the turn
            current = (current + 1) % PLAYERS
            clear()
            print_board(board)
            continue
        if check_win(board, token):
            clear()
            print_board(board)
            print(f"Player {token} won!")
            break
        if is_draw(board):
            clear()
            print_board(board)
            print("Draw!")
            break
        current = (current + 1) % PLAYERS
        clear()
        print_board(board)

if __name__ == "__main__":
    main()
