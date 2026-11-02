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
        row = []
        for _ in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    header = "  "
    for i in range(COLS):
        header += chr(ord('A') + i) + "   "
    print(header)
    line = "+---" * COLS + "+"
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def get_column_index(input_str):
    if len(input_str) != 1:
        return -1
    c = input_str[0]
    if c < 'A' or c >= chr(ord('A') + COLS):
        return -1
    return ord(c) - ord('A')

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_win(board, checker):
    # check horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # check vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # check diagonal /
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    # check diagonal \
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
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
        player = players[current]
        print(f"Player {player}, please enter a column:")
        inp = input().strip().upper()

        col = get_column_index(inp)
        if col == -1:
            print("Invalid column. Try again.")
            continue

        if not place_checker(board, col, player):
            print("Column full. You lose your turn.")
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
            
        print_board(board)

        if check_win(board, player):
            print(f"Player {player} won!")
            break

        if board_full(board):
            print("It's a draw!")
            break

        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
