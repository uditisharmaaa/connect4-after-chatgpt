import os
import random

# Constants for dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLUMNS))
    separator = '+---' * COLUMNS + '+'
    print(header)
    for row in board:
        print(separator)
        print('| ' + ' | '.join(row) + ' |')
    print(separator)

def valid_input(input_char, board):
    if len(input_char) == 1 and 'A' <= input_char.upper() < chr(ord('A') + COLUMNS):
        column = ord(input_char) - ord('A')
        return board[0][column] == ' '
    return False

def place_checker(board, column, symbol):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = symbol
            return

def check_consecutive_four(sequence):
    count = 0
    last_symbol = ' '
    for symbol in sequence:
        if symbol == last_symbol and symbol != ' ':
            count += 1
            if count == 4:
                return True
        else:
            count = 1
            last_symbol = symbol
    return False

def check_win(board):
    for row in board:
        if check_consecutive_four(row):
            return True

    for col in range(COLUMNS):
        if check_consecutive_four([board[row][col] for row in range(ROWS)]):
            return True

    for row in range(ROWS):
        for col in range(COLUMNS):
            if row + 3 < ROWS and col + 3 < COLUMNS and check_consecutive_four([board[row + i][col + i] for i in range(4)]):
                return True
            if row - 3 >= 0 and col + 3 < COLUMNS and check_consecutive_four([board[row - i][col + i] for i in range(4)]):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    board = create_board()
    current_player = random.choice(range(NUM_PLAYERS))
    print_board(board)

    while True:
        player_symbol = PLAYER_SYMBOLS[current_player]
        while True:
            column_letter = input(f"Player {player_symbol}, please enter a column: ").upper()
            if valid_input(column_letter, board):
                break
            print("Invalid input. Please try again.")

        column = ord(column_letter) - ord('A')
        place_checker(board, column, player_symbol)
        print_board(board)

        if check_win(board):
            print(f"Player {player_symbol} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

play_game()
