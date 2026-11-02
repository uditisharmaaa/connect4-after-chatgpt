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
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    header = "  "
    for i in range(COLS):
        header += " " + letters[i] + "  "
    print(header)
    sep = "+" + "---+" * COLS
    for r in range(ROWS):
        print(sep)
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
    print(sep)

def input_column():
    while True:
        col = input("Please enter a column: ").strip().upper()
        if len(col) != 1:
            print("Invalid input. Enter a single letter.")
            continue
        if col < 'A' or col >= chr(ord('A') + COLS):
            print("Invalid column. Try again.")
            continue
        return ord(col) - ord('A')

def place_checker(board, col, checker):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_win(board, checker):
    # check horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # check vertical
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # check diagonal up-right
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
    player_checkers = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    while True:
        print("Player " + player_checkers[current_player] + ", please enter a column:")
        col = input_column()
        placed = place_checker(board, col, player_checkers[current_player])
        if not placed:
            print("Column full. You lose your turn.")
        else:
            print_board(board)
            if check_win(board, player_checkers[current_player]):
                print("Player " + player_checkers[current_player] + " won!")
                break
            if check_draw(board):
                print("The game is a draw.")
                break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
