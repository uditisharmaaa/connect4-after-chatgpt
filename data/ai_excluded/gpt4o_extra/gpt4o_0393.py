import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def clear_screen():
    os.system('clear')

def print_board(board):
    header = '  ' + '   '.join(chr(65 + i) for i in range(len(board[0])))
    print(header)
    for row in board:
        print('+---' * len(row) + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * len(board[0]) + '+')

def select_random_player():
    return random.randint(0, PLAYERS_COUNT - 1)

def validate_input(input_char, columns):
    if len(input_char) != 1 or not input_char.isalpha():
        return False
    index = ord(input_char.upper()) - 65
    if index < 0 or index >= columns:
        return False
    return True

def place_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            return True
    return False

def check_winner(board, checker):
    for row in range(ROWS):
        for column in range(COLUMNS):
            if (
                column + 3 < COLUMNS and
                all(board[row][column + i] == checker for i in range(4))
            ):
                return True
            if (
                row + 3 < ROWS and
                all(board[row + i][column] == checker for i in range(4))
            ):
                return True
            if (
                column + 3 < COLUMNS and row + 3 < ROWS and
                all(board[row + i][column + i] == checker for i in range(4))
            ):
                return True
            if (
                column - 3 >= 0 and row + 3 < ROWS and
                all(board[row + i][column - i] == checker for i in range(4))
            ):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Initialize board
    board = initialize_board(ROWS, COLUMNS)

    # Randomly select the first player
    current_player = select_random_player()
    
    while True:
        clear_screen()
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")

        while True:
            column_choice = input("Column: ").strip()
            if validate_input(column_choice, COLUMNS):
                column_index = ord(column_choice.upper()) - 65
                if place_checker(board, column_index, CHECKERS[current_player]):
                    break
                else:
                    print("Column is full! Choose another column.")
            else:
                print("Invalid input! Please enter a valid column letter.")

        if check_winner(board, CHECKERS[current_player]):
            clear_screen()
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break
        
        # Alternate players
        current_player = (current_player + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
