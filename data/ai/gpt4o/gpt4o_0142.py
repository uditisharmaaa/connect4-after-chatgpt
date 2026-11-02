import random
import os

# Constants for board and players
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(c) for c in range(ord('A'), ord('A') + len(board[0]))))
    for row in board:
        print('+---' * len(row) + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * len(board[0]) + '+')

def is_valid_input(input_char, columns):
    return input_char.isalpha() and ord(input_char.upper()) - ord('A') < columns

def place_checker(board, column, checker):
    column_index = ord(column.upper()) - ord('A')
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            return True
    return False

def check_for_win(board, checker):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if (check_direction(board, checker, row, col, 1, 0) or  # Horizontal
                check_direction(board, checker, row, col, 0, 1) or  # Vertical
                check_direction(board, checker, row, col, 1, 1) or  # Diagonal /
                check_direction(board, checker, row, col, 1, -1)): # Diagonal \
                return True
    return False

def check_direction(board, checker, row, col, row_inc, col_inc):
    count = 0
    for i in range(4):
        r, c = row + i * row_inc, col + i * col_inc
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
        else:
            break
    return count == 4

def check_for_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYER_COUNT - 1)
    print_board(board)
    
    while True:
        current_checker = CHECKERS[current_player]
        input_column = input(f"Player {current_checker}, please enter a column: ")

        while not is_valid_input(input_column, COLUMNS) or not place_checker(board, input_column, current_checker):
            input_column = input(f"Invalid input. Player {current_checker}, please enter a column: ")

        print_board(board)

        if check_for_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        elif check_for_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYER_COUNT

# Starting the game
play_game()
