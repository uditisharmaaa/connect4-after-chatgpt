import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear(): os.system('clear')

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

def place_checker(board, col, checker):
    c = ord(col)-ord('A')
    for r in reversed(range(ROWS)):
        if board[r][c] == " ":
            board[r][c] = checker
            return True
    return False  # column full

def win_check(board, checker):
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
    # diagonal /
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    # diagonal \
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    return False

def full_board(board):
    return all(board[0][c] != " " for c in range(COLS))

def next_player(current):
    return (current +1) % PLAYERS

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = players[current]
        col = input(f"Player {checker}, please enter a column: ").strip().upper()
        if not valid_input(col):
            continue
        if not place_checker(board, col, checker):
            current = next_player(current)  # loses turn if column full
            print_board(board)
            continue
        print_board(board)
        if win_check(board, checker):
            print(f"Player {checker} won!")
            break
        if full_board(board):
            print("Game is a draw!")
            break
        current = next_player(current)

if __name__ == "__main__":
    main()
