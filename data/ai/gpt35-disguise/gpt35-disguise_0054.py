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
    letters = ""
    for c in range(COLS):
        letters += "  " + chr(ord('A') + c) + " "
    print(letters)
    line = "+---" * COLS + "+"
    for r in range(ROWS):
        print(line)
        row_str = ""
        for c in range(COLS):
            row_str += "| " + board[r][c] + " "
        print(row_str + "|")
    print(line)

def is_valid_input(inp):
    if len(inp) != 1:
        return False
    if inp < 'A' or inp >= chr(ord('A') + COLS):
        return False
    return True

def place_checker(board, col, checker):
    # start from bottom row and go up
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False # column full

def check_win(board, checker):
    # horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS -1)
    while True:
        print_board(board)
        print("Player {}, please enter a column:".format(players[current]))
        inp = input().strip().upper()

        if not is_valid_input(inp):
            continue
        col = ord(inp) - ord('A')
        if not place_checker(board, col, players[current]):
            # lose turn if column full
            current = (current +1) % PLAYERS
            continue

        if check_win(board, players[current]):
            print_board(board)
            print("Player {} won!".format(players[current]))
            break

        if board_full(board):
            print_board(board)
            print("Draw!")
            break

        current = (current +1) % PLAYERS


if __name__ == "__main__":
    main()
