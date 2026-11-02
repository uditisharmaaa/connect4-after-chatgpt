import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYER_COUNT]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLUMNS))
    print(header)
    print('+---' * COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLUMNS + '+')

def is_valid_input(column):
    return len(column) == 1 and column.isalpha() and 'A' <= column <= chr(ord('A') + COLUMNS - 1)

def is_column_full(board, col_index):
    return board[0][col_index] != ' '

def place_checker(board, col_index, checker):
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return True
    return False

def check_for_win(board, checker):
    # Check horizontal line
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True

    # Check vertical line
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal line (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal line (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.choice(range(PLAYER_COUNT))
    
    print_board(board)
    
    while True:
        current_checker = CHECKERS[current_player_index]
        column = input(f"Player {current_checker}, please enter a column: ").upper()
        
        if not is_valid_input(column):
            print("Invalid input! Please enter a valid column letter.")
            continue
        
        col_index = ord(column) - ord('A')
        
        if is_column_full(board, col_index):
            print("Column is full! You lose your turn.")
            current_player_index = (current_player_index + 1) % PLAYER_COUNT
            continue
        
        place_checker(board, col_index, current_checker)
        
        print_board(board)
        
        if check_for_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if check_for_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYER_COUNT

play_game()
