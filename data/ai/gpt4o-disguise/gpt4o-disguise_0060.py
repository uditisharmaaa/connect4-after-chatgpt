import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def is_valid_input(col, board):
    return len(col) == 1 and col.isalpha() and col.upper() in [chr(65 + i) for i in range(COLS)] and board[0][ord(col.upper()) - 65] == " "

def place_checker(board, col, checker):
    for i in range(ROWS-1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = checker
            break

def check_win(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                # horizontal
                if col <= COLS - 4 and all(board[row][col+i] == checker for i in range(4)):
                    return True
                # vertical
                if row <= ROWS - 4 and all(board[row+i][col] == checker for i in range(4)):
                    return True
                # diagonal /
                if row <= ROWS - 4 and col >= 3 and all(board[row+i][col-i] == checker for i in range(4)):
                    return True
                # diagonal \
                if row <= ROWS - 4 and col <= COLS - 4 and all(board[row+i][col+i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    print_board(board)
    current_player = random.randint(0, PLAYERS - 1)
    while True:
        print("Player", CHECKERS[current_player], "please enter a column:")
        col = input().strip()
        if not is_valid_input(col, board):
            print("Invalid input, try again.")
            continue
        col_idx = ord(col.upper()) - 65
        place_checker(board, col_idx, CHECKERS[current_player])
        print_board(board)
        if check_win(board, CHECKERS[current_player]):
            print("Player", CHECKERS[current_player], "won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
