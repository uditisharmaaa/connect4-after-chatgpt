import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    header = "  "
    for c in range(COLS):
        header += chr(ord('A') + c) + "   "
    print(header)
    for r in range(ROWS):
        line = "+"
        for c in range(COLS):
            line += "---+"
        print(line)
        row_line = "|"
        for c in range(COLS):
            row_line += " " + board[r][c] + " |"
        print(row_line)
    print("+" + "---+" * COLS)

def get_column_index(inp):
    if len(inp) != 1:
        return -1
    c = inp[0]
    if c < 'A' or c >= chr(ord('A') + COLS):
        return -1
    return ord(c) - ord('A')

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def win_check(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r][c+1] == checker and
                board[r][c+2] == checker and board[r][c+3] == checker):
                return True
    # vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if (board[r][c] == checker and board[r+1][c] == checker and
                board[r+2][c] == checker and board[r+3][c] == checker):
                return True
    # diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and board[r+3][c+3] == checker):
                return True
    # diagonal down-left
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if (board[r][c] == checker and board[r+1][c-1] == checker and
                board[r+2][c-2] == checker and board[r+3][c-3] == checker):
                return True
    return False

def full_board(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS - 1)
    print_board(board)
    while True:
        print("Player {}, please enter a column:".format(players[current]))
        inp = input().strip().upper()
        col = get_column_index(inp)
        if col == -1:
            continue  # invalid input, ask again
        if not place_checker(board, col, players[current]):
            # column full, loses turn
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if win_check(board, players[current]):
            print("Player {} won!".format(players[current]))
            break
        if full_board(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
