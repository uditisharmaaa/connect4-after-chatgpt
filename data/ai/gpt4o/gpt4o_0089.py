import os
import random

# Constants for game configuration
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Maximum 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = ' ' + '   '.join(chr(65 + i) for i in range(COLUMNS))
    print(column_labels)
    for row in board:
        print('+---' * COLUMNS + '+')
        print('|' + '|'.join(f' {col} ' for col in row) + '|')
    print('+---' * COLUMNS + '+')

def is_valid_input(column_choice):
    return column_choice.isalpha() and column_choice.upper() in [chr(65 + i) for i in range(COLUMNS)]

def drop_checker(board, column, checker):
    col_index = ord(column) - 65
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal, vertical, and diagonal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = CHECKERS[current_player]
        column_choice = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        while not is_valid_input(column_choice):
            column_choice = input(f"Invalid input. Player {current_checker}, please enter a valid column: ").strip().upper()

        if drop_checker(board, column_choice, current_checker):
            print_board(board)

            if check_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            if check_draw(board):
                print("The game is a draw!")
                break

            current_player = (current_player + 1) % PLAYERS
        else:
            print(f"Column {column_choice} is full. Player {current_checker} loses the turn.")
        
if __name__ == "__main__":
    main()
