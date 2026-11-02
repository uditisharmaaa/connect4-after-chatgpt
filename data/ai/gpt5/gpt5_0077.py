import os, random, string

# Constants (set for submission)
ROWS, COLS = 6, 7
NUM_PLAYERS = 2  # supports 2 to 5
CHECKERS = ["X", "O", "V", "H", "M"]

assert 2 <= NUM_PLAYERS <= 5 and 1 <= COLS <= 26

def create_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear_and_print(board):
    os.system('clear')
    letters = list(string.ascii_uppercase[:len(board[0])])
    print("  " + "   ".join(letters))
    print("+" + ("---+" * len(letters)))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + ("---+" * len(letters)))

def get_column_input(max_col):
    while True:
        s = input().strip().upper()
        if len(s) == 1 and "A" <= s <= chr(ord('A') + max_col - 1):
            return ord(s) - ord('A')
        print("Invalid input. Please enter a valid column letter:")

def drop_checker(board, col, ch):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = ch
            return r, col
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(board, r, c):
    ch = board[r][c]
    if ch == " ":
        return False
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    R, C = len(board), len(board[0])
    for dr, dc in directions:
        count = 1
        for s in (1, -1):
            nr, nc = r + s*dr, c + s*dc
            while in_bounds(nr, nc, R, C) and board[nr][nc] == ch:
                count += 1
                if count >= 4:
                    return True
                nr += s*dr
                nc += s*dc
    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    turn = random.randrange(NUM_PLAYERS)
    last_move = None
    while True:
        clear_and_print(board)
        if last_move and check_win(board, *last_move):
            print(f"Player {board[last_move[0]][last_move[1]]} won!")
            return
        if board_full(board):
            print("It's a draw!")
            return
        current = players[turn]
        print(f"Player {current}, please enter a column:")
        col = get_column_input(COLS)
        pos = drop_checker(board, col, current)
        if pos is None:
            print("Column is full. Turn lost. Press Enter to continue...")
            input()
        else:
            last_move = pos
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
