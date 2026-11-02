import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = '   '.join(chr(ord('A') + i) for i in range(COLUMNS))
    print(f"  {header}")
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def is_valid_input(input_char):
    return input_char.isalpha() and 'A' <= input_char <= chr(ord('A') + COLUMNS - 1)

def place_checker(board, column, checker):
    column_index = ord(column) - ord('A')
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            return True
    return False

def check_for_win(board, checker):
    # Horizontal check
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col:col + 4] == [checker] * 4:
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal check /
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Diagonal check \
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        print_board(board)
        player_checker = CHECKERS[current_player]
        print(f"Player {player_checker}, please enter a column:")

        column = input().strip().upper()
        while not is_valid_input(column) or not place_checker(board, column, player_checker):
            print("Invalid input or column full. Please enter another column:")
            column = input().strip().upper()

        if check_for_win(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break

        if check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
