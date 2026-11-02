import os, random

ROWS, COLS = 6, 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear(): os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(65+i) for i in range(COLS)))
    print("+" + "---+"*COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+"*COLS)

def valid_input(col):
    return len(col) == 1 and 'A' <= col <= chr(65+COLS-1)

def place_checker(board, col, checker):
    c = ord(col) - 65
    for r in reversed(range(ROWS)):
        if board[r][c] == " ":
            board[r][c] = checker
            return True
    return False

def check_win(board, checker):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    # Diagonal \
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    return False

def board_full(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYER_COUNT]
    current = random.randint(0, PLAYER_COUNT-1)
    while True:
        print_board(board)
        print(f"Player {players[current]}, please enter a column:")
        col = input().strip().upper()
        if not valid_input(col):
            continue
        if not place_checker(board, col, players[current]):
            current = (current + 1) % PLAYER_COUNT
            continue
        if check_win(board, players[current]):
            print_board(board)
            print(f"Player {players[current]} won!")
            break
        if board_full(board):
            print_board(board)
            print("The game is a draw.")
            break
        current = (current + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
