import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    clear_screen()
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def valid_input(col):
    if len(col) != 1:
        return False
    c = col.upper()
    if c < 'A' or c >= chr(ord('A') + COLS):
        return False
    return True

def find_row(board, col):
    for r in reversed(range(ROWS)):
        if board[r][col] == " ":
            return r
    return -1

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def check_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = PLAYERS
    checkers = CHECKERS[:players]
    current = random.randint(0, players -1)

    print_board(board)

    while True:
        print("Player " + checkers[current] + ", please enter a column:")
        inp = input().strip().upper()
        if not valid_input(inp):
            continue
        col = ord(inp) - ord('A')
        row = find_row(board, col)
        if row == -1:
            current = (current + 1) % players
            continue
        board[row][col] = checkers[current]
        print_board(board)
        if check_win(board, checkers[current]):
            print("Player " + checkers[current] + " won!")
            break
        if check_draw(board):
            print("Game is a draw!")
            break
        current = (current + 1) % players

if __name__ == "__main__":
    main()
