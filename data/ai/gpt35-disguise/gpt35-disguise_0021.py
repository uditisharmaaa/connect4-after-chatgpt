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
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("  ", end="")
    for i in range(COLS):
        print(" "+letters[i]+" ", end=" ")
    print()
    for r in range(ROWS):
        print("+" + "---+"*COLS)
        print("|", end="")
        for c in range(COLS):
            print(" "+board[r][c]+" |", end="")
        print()
    print("+" + "---+"*COLS)

def get_player_move(player, board):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        move = input(f"Player {CHECKERS[player]}, please enter a column: ")
        if len(move) != 1:
            continue
        if move not in letters[:COLS]:
            continue
        col = letters.index(move)
        if board[0][col] != " ":
            # column full, lose turn
            print("Column full, you lose your turn.")
            return -1
        return col

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1

def check_winner(board, checker):
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
    # diagonal down right
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up right
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
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        col = get_player_move(current_player, board)
        if col == -1:
            # lose turn
            current_player = (current_player +1) % PLAYERS
            print_board(board)
            continue
        row, col = place_checker(board, col, CHECKERS[current_player])
        print_board(board)
        if check_winner(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("Draw!")
            break
        current_player = (current_player +1) % PLAYERS

if __name__ == "__main__":
    main()
