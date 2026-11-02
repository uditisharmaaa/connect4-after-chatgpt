import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    
    print("  " + "   ".join(chr(65+i) for i in range(COLS)))
    print("+---" * COLS + "+")
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(col, board):
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def drop_checker(board, row, col, checker):
    board[row][col] = checker

def check_win(board, checker):
    # Check horizontal locations
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] == checker:
                return True

    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] == checker:
                return True

    return False

def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = create_board()
    print_board(board)
    game_over = False
    turn = random.randint(0, PLAYERS - 1)

    while not game_over:
        print_board(board)
        print(f"Player {CHECKERS[turn]}, please enter a column:")

        col = input().strip().upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input. Please enter a letter corresponding to a column.")
            continue

        col = ord(col) - 65

        if not is_valid_column(col, board):
            print("Column full or invalid. Please choose another column.")
            continue
        
        row = get_next_open_row(board, col)
        if row is not None:
            drop_checker(board, row, col, CHECKERS[turn])

            if check_win(board, CHECKERS[turn]):
                print_board(board)
                print(f"Player {CHECKERS[turn]} won!")
                game_over = True
            elif is_draw(board):
                print_board(board)
                print("The game is a draw!")
                game_over = True
            else:
                turn = (turn + 1) % PLAYERS
    
if __name__ == "__main__":
    main()
