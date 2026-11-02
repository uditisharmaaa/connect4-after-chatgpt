import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def clear(): os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  "+"   ".join(chr(65+i) for i in range(COLS)))
    print("+---"*COLS+"+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS+"+")

def valid_column(col):
    return col.isalpha() and col.upper() >= 'A' and col.upper() < chr(65+COLS)

def place_checker(board, col, checker):
    c = ord(col.upper()) - 65
    for r in range(ROWS-1, -1, -1):
        if board[r][c] == " ":
            board[r][c] = checker
            return True
    return False

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != checker:
                continue
            # Horizontal
            if c + 3 < COLS and all(board[r][c+i] == checker for i in range(4)):
                return True
            # Vertical
            if r + 3 < ROWS and all(board[r+i][c] == checker for i in range(4)):
                return True
            # Diagonal /
            if r - 3 >= 0 and c + 3 < COLS and all(board[r-i][c+i] == checker for i in range(4)):
                return True
            # Diagonal \
            if r + 3 < ROWS and c + 3 < COLS and all(board[r+i][c+i] == checker for i in range(4)):
                return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = CHECKERS[current]
        inp = input(f"Player {checker}, please enter a column: ").strip()
        if not valid_column(inp):
            continue
        if not place_checker(board, inp, checker):
            # column full lose turn
            current = (current + 1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
