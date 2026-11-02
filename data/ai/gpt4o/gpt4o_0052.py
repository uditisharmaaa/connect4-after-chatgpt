import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear the console
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def is_valid_column(column_choice, board):
    if column_choice.isalpha() and len(column_choice) == 1:
        col_index = ord(column_choice.upper()) - 65
        if 0 <= col_index < COLUMNS and board[0][col_index] == ' ':
            return True
    return False

def get_column_index(column_choice):
    return ord(column_choice.upper()) - 65

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def has_winner(board, checker):
    # Horizontal Check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Vertical Check
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Positive Diagonal Check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Negative Diagonal Check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    num_moves = 0

    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column_choice = input().strip()

        if not is_valid_column(column_choice, board):
            print("Invalid column. Please try again.")
            continue
        
        column_index = get_column_index(column_choice)
        place_checker(board, column_index, CHECKERS[current_player])
        num_moves += 1
        print_board(board)

        if has_winner(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
