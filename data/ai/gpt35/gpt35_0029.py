import os
import random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O']  # only 2 players for submission
WIN_LEN = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    line = '+---' * COLS + '+'
    for row in board:
        print(line)
        print('| ' + ' | '.join(row) + ' |')
    print(line)

def valid_input(inp):
    return len(inp) == 1 and 'A' <= inp <= chr(ord('A') + COLS - 1)

def place_checker(board, col, checker):
    for r in reversed(range(ROWS)):
        if board[r][col] == ' ':
            board[r][col] = checker
            return True
    return False  # column full

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - WIN_LEN + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LEN)):
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS - WIN_LEN + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LEN)):
                return True
    # diagonal down-right
    for r in range(ROWS - WIN_LEN + 1):
        for c in range(COLS - WIN_LEN + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LEN)):
                return True
    # diagonal down-left
    for r in range(ROWS - WIN_LEN + 1):
        for c in range(WIN_LEN - 1, COLS):
            if all(board[r + i][c - i] == checker for i in range(WIN_LEN)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    current = random.randint(0, len(PLAYERS) - 1)
    print_board(board)

    while True:
        checker = PLAYERS[current]
        inp = input(f"Player {checker}, please enter a column: ").upper()
        if not valid_input(inp):
            continue
        col = ord(inp) - ord('A')
        if not place_checker(board, col, checker):
            current = (current + 1) % len(PLAYERS)
            print_board(board)
            continue  # lose turn if col full
        print_board(board)
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("Game is a draw!")
            break
        current = (current + 1) % len(PLAYERS)

if __name__ == '__main__':
    main()
