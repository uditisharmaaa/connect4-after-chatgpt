import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
    os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    print("+---"*COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS + "+")

def valid_input(col):
    return len(col) == 1 and 'A' <= col <= chr(ord('A')+COLS-1)

def place_checker(board, col_idx, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return True
    return False  # column full

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # diag \
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # diag /
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = players[current]
        print(f"Player {checker}, please enter a column:")
        col = input().strip().upper()
        if not valid_input(col):
            continue
        col_idx = ord(col) - ord('A')
        if not place_checker(board, col_idx, checker):
            # full column => lose turn
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
