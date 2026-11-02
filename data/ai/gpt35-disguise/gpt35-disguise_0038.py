import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear()
    letters = [chr(ord("A")+i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    for r in range(ROWS):
        print("+" + "---+"*COLS)
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
    print("+" + "---+"*COLS)

def get_valid_input(board, player):
    letters = [chr(ord("A")+i) for i in range(COLS)]
    while True:
        print(f"Player {CHECKERS[player]}, please enter a column:")
        col = input().upper()
        if len(col) != 1:
            continue
        if col not in letters:
            continue
        col_idx = ord(col) - ord("A")
        # Check if column full
        if board[0][col_idx] != " ":
            # turn lost
            return -1
        return col_idx

def place_checker(board, col_idx, checker):
    for r in reversed(range(ROWS)):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r, col_idx

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    player = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        col_idx = get_valid_input(board, player)
        if col_idx == -1:
            # Column full, turn lost
            player = (player + 1) % PLAYERS
            print_board(board)
            continue
        place_checker(board, col_idx, CHECKERS[player])
        print_board(board)
        if check_win(board, CHECKERS[player]):
            print(f"Player {CHECKERS[player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        player = (player + 1) % PLAYERS

main()
