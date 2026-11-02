import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4

def clear(): os.system('clear')

def create_board(): return [[" "]*COLS for _ in range(ROWS)]

def print_board(b):
    clear()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    print("+---"*COLS + "+")
    for r in range(ROWS):
        print("| " + " | ".join(b[r]) + " |")
        print("+---"*COLS + "+")

def valid_column(c):
    return len(c) == 1 and 'A' <= c <= chr(ord('A')+COLS-1)

def place_checker(board, col, checker):
    c = ord(col) - ord('A')
    for r in range(ROWS-1, -1, -1):
        if board[r][c] == " ":
            board[r][c] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != checker:
                continue
            # Horizontal
            if c+WIN_CONDITION <= COLS and all(board[r][c+i] == checker for i in range(WIN_CONDITION)):
                return True
            # Vertical
            if r+WIN_CONDITION <= ROWS and all(board[r+i][c] == checker for i in range(WIN_CONDITION)):
                return True
            # Diagonal down-right
            if r+WIN_CONDITION <= ROWS and c+WIN_CONDITION <= COLS and all(board[r+i][c+i] == checker for i in range(WIN_CONDITION)):
                return True
            # Diagonal down-left
            if r+WIN_CONDITION <= ROWS and c-WIN_CONDITION+1 >= 0 and all(board[r+i][c-i] == checker for i in range(WIN_CONDITION)):
                return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randrange(PLAYERS)
    print_board(board)
    while True:
        checker = players[current]
        col = input(f"Player {checker}, please enter a column: ").upper()
        if not valid_column(col):
            continue
        if not place_checker(board, col, checker):
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("The game is a draw.")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
