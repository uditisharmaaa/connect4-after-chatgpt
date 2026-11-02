import os, random, sys

# Constants (submission must be 6x7 and 2 players)
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # supports 2..5 players
TOKENS = ["X", "O", "V", "H", "M"]

assert 2 <= NUM_PLAYERS <= 5
assert 1 <= COLS <= 26

LETTERS = [chr(ord('A') + i) for i in range(COLS)]

def create_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(board):
    r, c = len(board), len(board[0])
    header = "  " + "   ".join(LETTERS[:c])
    hline = "+" + ("---+" * c)
    print(header)
    for row in range(r):
        print(hline)
        line = "|"
        for col in range(c):
            line += f" {board[row][col]} |"
        print(line)
    print(hline)

def drop_checker(board, col_idx, token):
    # place from bottom up; return True if placed, False if column full
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = token
            return True
    return False

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(board, token):
    R, C = len(board), len(board[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(R):
        for c in range(C):
            if board[r][c] != token:
                continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r, c
                for _ in range(3):
                    rr += dr; cc += dc
                    if not in_bounds(rr, cc, R, C) or board[rr][cc] != token:
                        break
                    cnt += 1
                if cnt == 4:
                    return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def get_valid_input():
    while True:
        s = input().strip()
        if len(s) != 1:
            print("Invalid input. Enter a single column letter:")
            continue
        ch = s.upper()
        if ch not in LETTERS:
            print("Invalid column. Enter a letter from", LETTERS[0], "to", LETTERS[-1], ":")
            continue
        return LETTERS.index(ch), ch

def main():
    board = create_board(ROWS, COLS)
    players = TOKENS[:NUM_PLAYERS]
    turn = random.randrange(NUM_PLAYERS)

    # Show initial empty board before the first move
    clear()
    print_board(board)

    while True:
        token = players[turn]
        print(f"Player {token}, please enter a column:")
        col_idx, col_char = get_valid_input()

        placed = drop_checker(board, col_idx, token)
        if not placed:
            # Column full: turn is invalid and player loses the turn
            print(f"Column {col_char} is full. Turn lost.")
            turn = (turn + 1) % NUM_PLAYERS
        else:
            # Check game state after a successful move
            if check_win(board, token):
                clear()
                print_board(board)
                print(f"Player {token} won!")
                break
            if board_full(board):
                clear()
                print_board(board)
                print("It's a draw!")
                break
            turn = (turn + 1) % NUM_PLAYERS

        # Show updated board for next player's turn
        clear()
        print_board(board)

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)
