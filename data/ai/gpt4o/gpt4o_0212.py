import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    column_labels = ' '.join([chr(ord('A') + i) for i in range(len(board[0]))])
    print(f"  {column_labels}")
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def get_column_input(players_checker):
    while True:
        input_column = input(f"Player {players_checker}, please enter a column: ").strip().upper()
        if len(input_column) == 1 and 'A' <= input_column < chr(ord('A') + COLUMNS):
            return ord(input_column) - ord('A')
        print("Invalid input. Please enter a valid column letter.")

def place_checker(board, column, player_checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player_checker
            return True
    return False

def check_winner(board, player_checker):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (
                col <= COLUMNS - 4 and all(board[row][col + i] == player_checker for i in range(4)) or
                row <= ROWS - 4 and all(board[row + i][col] == player_checker for i in range(4)) or
                row <= ROWS - 4 and col <= COLUMNS - 4 and all(board[row + i][col + i] == player_checker for i in range(4)) or
                row >= 3 and col <= COLUMNS - 4 and all(board[row - i][col + i] == player_checker for i in range(4))
            ):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)
    while True:
        current_checker = players[current_player_idx]
        column = get_column_input(current_checker)

        if place_checker(board, column, current_checker):
            print_board(board)

            if check_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break

            current_player_idx = (current_player_idx + 1) % PLAYERS
        else:
            print("Column is full, turn lost.")

play_game()
