import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players can be supported
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # ['A', 'B', ..., 'G'] for 7 columns

def clear_screen():
    # Clears the terminal screen for easier reading of board updates
    os.system('clear')

def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join([' ' + cell + ' ' for cell in row]) + '|')
        print('+---' * COLUMNS + '+')

def is_valid_input(column):
    return column in COLUMN_LABELS

def is_column_full(board, column_index):
    return board[0][column_index] != ' '

def place_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            break

def check_for_win(board, checker):
    # Check horizontal for win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical for win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def check_for_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = initialize_board()
    print_board(board)
    
    current_player = random.randint(0, PLAYERS - 1)
    winner = None

    while not winner:
        current_checker = CHECKERS[current_player]
        print(f"Player {current_checker}, please enter a column:")
        column_input = input().strip().upper()

        while not is_valid_input(column_input) or is_column_full(board, COLUMN_LABELS.index(column_input)):
            print(f"Invalid input, Player {current_checker}. Please enter a valid column:")
            column_input = input().strip().upper()
        
        column_index = COLUMN_LABELS.index(column_input)
        place_checker(board, column_index, current_checker)
        print_board(board)
        
        if check_for_win(board, current_checker):
            winner = current_checker
            print(f"Player {winner} won!")
            break
        
        if check_for_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == '__main__':
    main()
