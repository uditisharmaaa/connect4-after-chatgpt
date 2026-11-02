import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board, columns):
    os.system('clear')
    header = ' '.join(chr(65 + i) for i in range(columns))
    print(f'  {header}')
    print('+---' * columns + '+')
    for row in board:
        print('|' + '|'.join(f' {item} ' for item in row) + '|')
        print('+---' * columns + '+')

def check_valid_input(input_char, columns):
    return input_char.isalpha() and 'A' <= input_char < chr(65 + columns)

def get_empty_row(board, col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def check_winner(board, player):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (check_direction(board, row, col, player, 1, 0) or  # Horizontal
                check_direction(board, row, col, player, 0, 1) or  # Vertical
                check_direction(board, row, col, player, 1, 1) or  # Diagonal /
                check_direction(board, row, col, player, 1, -1)): # Diagonal \
                return True
    return False

def check_direction(board, row, col, player, row_direction, col_direction):
    try:
        return all(board[row + i * row_direction][col + i * col_direction] == player for i in range(4))
    except IndexError:
        return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player = random.choice(range(PLAYERS))
    print_board(board, COLUMNS)

    while True:
        player_char = CHECKERS[current_player]
        input_valid = False

        while not input_valid:
            choice = input(f"Player {player_char}, please enter a column: ").strip().upper()
            if check_valid_input(choice, COLUMNS):
                col_index = ord(choice) - 65
                row_index = get_empty_row(board, col_index)
                if row_index != -1:
                    board[row_index][col_index] = player_char
                    input_valid = True
                else:
                    print("Column is full. Turn lost.")
            else:
                print("Invalid input. Try again.")

        print_board(board, COLUMNS)

        if check_winner(board, player_char):
            print(f"Player {player_char} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

play_game()
