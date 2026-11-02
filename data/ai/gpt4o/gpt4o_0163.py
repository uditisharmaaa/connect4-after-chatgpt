import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    columns_header = '  ' + '   '.join(chr(65 + i) for i in range(len(board[0])))
    print(columns_header)
    for row in board:
        print('+---' * len(row) + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * len(board[0]) + '+')

def is_valid_input(input_char, columns):
    return input_char.isalpha() and 65 <= ord(input_char) < 65 + columns

def is_valid_move(board, column_index):
    return any(cell == ' ' for cell in [row[column_index] for row in board])

def place_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            return

def check_winner(board, checker):
    rows = len(board)
    columns = len(board[0])

    # Check horizontal
    for row in board:
        for col in range(columns - 3):
            if all(cell == checker for cell in row[col:col + 4]):
                return True

    # Check vertical
    for col in range(columns):
        for row in range(rows - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal /
    for row in range(rows - 3):
        for col in range(columns - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal \
    for row in range(rows - 3):
        for col in range(3, columns):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player = random.choice(range(NUM_PLAYERS))

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")

        while True:
            player_input = input().strip().upper()
            if is_valid_input(player_input, COLUMNS):
                column_index = ord(player_input) - 65
                if is_valid_move(board, column_index):
                    break
                else:
                    print("Column is full, try again.")
            else:
                print("Invalid input, try again.")

        place_checker(board, column_index, CHECKERS[current_player])

        if check_winner(board, CHECKERS[current_player]):
            clear_screen()
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        elif check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
