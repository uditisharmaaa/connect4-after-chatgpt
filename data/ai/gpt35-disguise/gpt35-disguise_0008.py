import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    os.system('clear')
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    header = "  "
    for i in range(COLS):
        header += " " + letters[i] + "  "
    print(header)
    line = "+---" * COLS + "+"
    for row in range(ROWS):
        print(line)
        row_str = "|"
        for col in range(COLS):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    print(line)

def is_valid_column(col_letter):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if col_letter in letters[:COLS]:
        return True
    return False

def column_index(col_letter):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return letters.index(col_letter)

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_winner(board, checker):
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
                
    # diagonal down right
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
                
    # diagonal up right
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
                
    return False

def board_full(board):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        player_check = players[current]
        print("Player " + player_check + ", please enter a column:")
        choice = input().strip().upper()
        if not is_valid_column(choice):
            continue
        col = column_index(choice)
        if board[0][col] != " ":
            current = (current + 1) % PLAYERS
            continue
        placed = place_checker(board, col, player_check)
        if not placed:
            current = (current + 1) % PLAYERS
            continue
        print_board(board)
        if check_winner(board, player_check):
            print("Player " + player_check + " won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
