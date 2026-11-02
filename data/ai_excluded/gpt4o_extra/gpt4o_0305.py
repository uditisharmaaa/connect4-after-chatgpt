import os
import random

# Constants for configuration
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLUMNS)]))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLUMNS + '+')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def select_first_player():
    return random.choice(CHECKERS)

def is_valid_input(column):
    return column.isalpha() and 'A' <= column <= chr(ord('A') + COLUMNS - 1)

def place_checker(board, player, column):
    col_index = ord(column) - ord('A')
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = player
            return True
    return False

def check_winner(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    board = create_board()
    current_player = select_first_player()

    while True:
        print_board(board)
        column = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        if not is_valid_input(column):
            print("Invalid input. Please enter a valid column letter.")
            continue

        if not place_checker(board, current_player, column):
            print("Column is full. Try another column.")
            continue

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]

# Start the game
if __name__ == "__main__":
    play_game()
