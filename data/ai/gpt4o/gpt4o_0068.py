import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLUMNS + '+')

def get_column_choice(player_symbol):
    while True:
        choice = input(f"Player {player_symbol}, please enter a column: ").upper()
        if choice.isalpha() and len(choice) == 1 and 'A' <= choice < chr(65 + COLUMNS):
            return ord(choice) - 65
        print("Invalid input. Please enter a valid column letter.")

def place_checker(board, column, player_symbol):
    # Attempt to place checker at the lowest available row in the chosen column
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player_symbol
            return True
    return False  # Column is full

def check_win(board, player_symbol):
    # Check horizontal win
    for row in board:
        for start in range(COLUMNS - 3):
            if all(cell == player_symbol for cell in row[start:start+4]):
                return True

    # Check vertical win
    for col in range(COLUMNS):
        for start in range(ROWS - 3):
            if all(board[start+i][col] == player_symbol for i in range(4)):
                return True

    # Check diagonal win (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == player_symbol for i in range(4)):
                return True

    # Check diagonal win (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board(ROWS, COLUMNS)
    num_players = 2  # This can be set to any number between 2 and MAX_PLAYERS
    player_symbols = PLAYER_SYMBOLS[:num_players]

    # Randomize first player
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)
    while True:
        current_player_symbol = player_symbols[current_player_index]
        column_choice = get_column_choice(current_player_symbol)
        
        if not place_checker(board, column_choice, current_player_symbol):
            print("Column is full. Turn lost.")
        else:
            print_board(board)
            
            if check_win(board, current_player_symbol):
                print(f"Player {current_player_symbol} won!")
                break

            if check_draw(board):
                print("The game is a draw.")
                break
            
        # Switch to next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == '__main__':
    main()
