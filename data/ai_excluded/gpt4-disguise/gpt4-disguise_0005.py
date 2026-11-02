import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(ALPHABET[:COLS])
    print(header)
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_column(col, board):
    if col not in ALPHABET[:COLS]:
        return False
    col_index = ALPHABET.index(col)
    return board[0][col_index] == " "

def get_lowest_empty_row(board, col_index):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            return row
    return -1

def place_checker(board, col, checker):
    col_index = ALPHABET.index(col)
    row = get_lowest_empty_row(board, col_index)
    if row != -1:
        board[row][col_index] = checker

def check_sequence(seq, checker):
    count = 0
    for cell in seq:
        if cell == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def check_win(board, checker):
    # Horizontal check
    for row in board:
        if check_sequence(row, checker):
            return True
    # Vertical check
    for col in range(COLS):
        column = [board[row][col] for row in range(ROWS)]
        if check_sequence(column, checker):
            return True
    # Diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Diagonal (bottom-right to top-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    
    print_board(board)
    while True:
        print(f"Player {current_player}, please enter a column:")
        col = input().strip().upper()
        
        if not is_valid_column(col, board):
            print("Invalid column. Try again.")
            continue
        
        place_checker(board, col, current_player)
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
