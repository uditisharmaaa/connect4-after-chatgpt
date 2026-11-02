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
        row = [" "]*COLS
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    header = "  "
    for i in range(COLS):
        header += " " + chr(ord('A') + i) + "  "
    print(header)
    line = "+---"*COLS + "+"
    for r in range(ROWS):
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def input_column(player):
    while True:
        s = input("Player " + player + ", please enter a column: ")
        if len(s) != 1:
            print("Invalid input. Enter one letter corresponding to a column.")
            continue
        c = s[0]
        if c < 'A' or c >= chr(ord('A') + COLS):
            print("Invalid column. Enter a letter from A to " + chr(ord('A') + COLS -1) + ".")
            continue
        return ord(c) - ord('A')

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # column full

def winner_check(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS -3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right
    for r in range(ROWS -3):
        for c in range(COLS -3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal down-left
    for r in range(ROWS -3):
        for c in range(3, COLS):
            if board[r][c] == checker and board[r+1][c-1] == checker and board[r+2][c-2] == checker and board[r+3][c-3] == checker:
                return True
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        checker = players[current]
        col = input_column(checker)
        placed = place_checker(board, col, checker)
        if not placed:
            print("Column full. You lose your turn.")
        print_board(board)
        if placed:
            if winner_check(board, checker):
                print("Player " + checker + " won!")
                break
            if board_full(board):
                print("Game is a draw!")
                break
        current = (current +1) % PLAYERS

if __name__ == "__main__":
    main()
