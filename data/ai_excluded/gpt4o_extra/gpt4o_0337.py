import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    column_labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:len(board[0])]
    print('  ' + '   '.join(column_labels))
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * len(board[0]) + '+')

def is_valid_input(column, board):
    if column.isalpha() and len(column) == 1:
        col_index = ord(column.upper()) - ord('A')
        if 0 <= col_index < len(board[0]) and board[0][col_index] == ' ':
            return True
    return False

def drop_checker(board, column, checker):
    col_index = ord(column.upper()) - ord('A')
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return

def check_for_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonals
    for col in range(len(board[0]) - 3):
        for row in range(len(board) - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
        for row in range(3, len(board)):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    
    return False

def check_for_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    print_board(board)
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column = input().strip()

        if is_valid_input(column, board):
            drop_checker(board, column, CHECKERS[current_player])
            print_board(board)
            
            if check_for_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            elif check_for_draw(board):
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % PLAYERS
        else:
            print("Invalid input, try again!")

if __name__ == "__main__":
    main()
