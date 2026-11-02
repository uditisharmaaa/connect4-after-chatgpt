import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']
BOARD_WIDTH = 7
PLAYER_COUNT = 2

def clear_screen():
    os.system('clear')

def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = ' ' + '   '.join(chr(65 + i) for i in range(len(board[0])))
    separator = '+---' * len(board[0]) + '+'
    print(column_labels)
    for row in board:
        print(separator)
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
    print(separator)

def get_valid_column(board):
    while True:
        column_input = input("Please enter a column: ").strip().upper()
        if len(column_input) != 1 or not column_input.isalpha():
            print("Invalid input. Enter a single alphabetical character.")
            continue
        
        column_index = ord(column_input) - ord('A')
        if column_index < 0 or column_index >= len(board[0]):
            print("Invalid column. Choose a letter corresponding to a column.")
            continue
        
        if board[0][column_index] != ' ':
            print("Column is full. Choose another column.")
            continue
        
        return column_index

def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

def check_winner(board, checker):
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all(cell == checker for cell in row[i:i + 4]):
                return True

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal /
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal \
    for row in range(len(board) - 3):
        for col in range(3, len(board[0])):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYER_COUNT - 1)  # Randomly select a starting player

    while True:
        print_board(board)
        checker = PLAYERS[current_player]
        print(f"Player {checker}, it's your turn.")
        column = get_valid_column(board)
        drop_checker(board, column, checker)
        
        if check_winner(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
