import os, random, string

# Constants (changeable, but submit with these)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # 2..5
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def create_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    letters = string.ascii_uppercase[:len(board[0])]
    print("  " + "   ".join(letters))
    sep = "+" + "---+" * len(board[0])
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

def drop_checker(board, col, sym):
    # Place checker in lowest empty cell in the column; return row or None if full
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return r
    return None

def check_win(board):
    R, C = len(board), len(board[0])
    for r in range(R):
        for c in range(C):
            s = board[r][c]
            if s == " ":
                continue
            # horiz
            if c <= C-4 and all(board[r][c+i] == s for i in range(4)):
                return s
            # vert
            if r <= R-4 and all(board[r+i][c] == s for i in range(4)):
                return s
            # diag down-right
            if r <= R-4 and c <= C-4 and all(board[r+i][c+i] == s for i in range(4)):
                return s
            # diag up-right
            if r >= 3 and c <= C-4 and all(board[r-i][c+i] == s for i in range(4)):
                return s
    return None

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_column_input(valid_letters):
    while True:
        inp = input().strip().upper()
        if len(inp) == 1 and inp in valid_letters:
            return inp
        print(f"Invalid input. Please enter one of: {', '.join(valid_letters)}")

def main():
    board = create_board(ROWS, COLS)
    letters = string.ascii_uppercase[:COLS]
    current = random.randrange(NUM_PLAYERS)

    while True:
        print_board(board)
        print(f"Player {CHECKERS[current]}, please enter a column:")
        col_letter = get_column_input(letters)
        col = ord(col_letter) - ord('A')

        placed_row = drop_checker(board, col, CHECKERS[current])
        if placed_row is None:
            print_board(board)
            print(f"Column {col_letter} is full. Player {CHECKERS[current]} loses the turn.")
        else:
            winner = check_win(board)
            if winner:
                print_board(board)
                print(f"Player {winner} won!")
                break
            if is_draw(board):
                print_board(board)
                print("It's a draw!")
                break

        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
