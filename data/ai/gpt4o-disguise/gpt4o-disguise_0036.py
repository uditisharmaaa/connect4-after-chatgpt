import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    col_labels = '  ' + '   '.join(chr(65 + i) for i in range(COLUMNS))
    print(col_labels)
    for row in board:
        print('+---' * COLUMNS + '+')
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
    print('+---' * COLUMNS + '+')

def is_valid_input(inp):
    return inp.isalpha() and 'A' <= inp <= chr(65 + COLUMNS - 1)

def place_checker(board, column, checker):
    col_index = ord(column) - 65
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if vertical_win(board, r, c, checker) or horizontal_win(board, r, c, checker) or diagonal_win(board, r, c, checker):
                return True
    return False

def vertical_win(board, r, c, checker):
    if r + 3 < ROWS and all(board[r+i][c] == checker for i in range(4)):
        return True
    return False

def horizontal_win(board, r, c, checker):
    if c + 3 < COLUMNS and all(board[r][c+i] == checker for i in range(4)):
        return True
    return False

def diagonal_win(board, r, c, checker):
    if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r+i][c+i] == checker for i in range(4)):
        return True
    if r - 3 >= 0 and c + 3 < COLUMNS and all(board[r-i][c+i] == checker for i in range(4)):
        return True
    return False

def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.choice(range(PLAYERS))
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        while True:
            col = input().strip().upper()
            if is_valid_input(col):
                if place_checker(board, col, CHECKERS[current_player]):
                    break
                else:
                    print("Column is full, try another one:")
            else:
                print("Invalid input, try again:")
        
        print_board(board)

        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == '__main__':
    main()
