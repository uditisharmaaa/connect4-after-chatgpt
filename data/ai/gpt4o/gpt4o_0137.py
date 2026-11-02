import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = '  '.join(chr(ord('A') + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    for row in board:
        print('+---' * len(row) + '+')
        print('|' + ''.join(f" {cell} |" for cell in row))
    print('+---' * len(row) + '+')

def is_valid_input(input_char, columns):
    return input_char.isalpha() and 'A' <= input_char < chr(ord('A') + columns)

def place_checker(board, column, checker):
    column_index = ord(column) - ord('A')
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            return True
    return False

def check_winner(board, checker):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] != checker:
                continue
            for direction in directions:
                if all((0 <= row + direction[0] * i < ROWS and 
                        0 <= column + direction[1] * i < COLUMNS and 
                        board[row + direction[0] * i][column + direction[1] * i] == checker) for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board(ROWS, COLUMNS)
    turn = random.randint(0, PLAYERS - 1)
    current_checker = CHECKERS[turn]
    
    while True:
        print_board(board)
        input_column = input(f"Player {current_checker}, please enter a column: ").upper()
        
        while not is_valid_input(input_column, COLUMNS) or not place_checker(board, input_column, current_checker):
            print(f"Invalid input! Please enter a valid column between A and {chr(ord('A') + COLUMNS - 1)}.")
            input_column = input(f"Player {current_checker}, please enter a column: ").upper()
        
        if check_winner(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        turn = (turn + 1) % PLAYERS
        current_checker = CHECKERS[turn]

if __name__ == "__main__":
    play_game()
