import random
import os

# Constants
NUM_ROWS = 6
NUM_COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(chr(i) for i in range(ord('A'), ord('A') + len(board[0]))))
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def validate_input(user_input, max_column):
    if len(user_input) != 1 or not user_input.isalpha():
        return False
    column = ord(user_input.upper()) - ord('A')
    return 0 <= column < max_column

def place_checker(board, column, symbol):
    for i in range(len(board) - 1, -1, -1):
        if board[i][column] == ' ':
            board[i][column] = symbol
            return True
    return False

def check_win(board, symbol):
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLUMNS - 3):
            if all(board[r][c+i] == symbol for i in range(4)):
                return True
    # Check vertical
    for c in range(NUM_COLUMNS):
        for r in range(NUM_ROWS - 3):
            if all(board[r+i][c] == symbol for i in range(4)):
                return True
    # Check diagonal /
    for r in range(3, NUM_ROWS):
        for c in range(NUM_COLUMNS - 3):
            if all(board[r-i][c+i] == symbol for i in range(4)):
                return True
    # Check diagonal \
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLUMNS - 3):
            if all(board[r+i][c+i] == symbol for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def connect4_game():
    board = create_board(NUM_ROWS, NUM_COLUMNS)
    num_players = 2  # Initial setting for a 2-player game
    current_player = random.randint(0, num_players - 1)
    game_ongoing = True

    print_board(board)

    while game_ongoing:
        current_symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {current_symbol}, please enter a column: ")

        user_input = input().strip()
        
        if not validate_input(user_input, NUM_COLUMNS):
            print("Invalid input. Please enter a valid column letter.")
            continue

        column = ord(user_input.upper()) - ord('A')

        if not place_checker(board, column, current_symbol):
            print("Column is full. Turn is lost.")
        else:
            print_board(board)
            if check_win(board, current_symbol):
                print(f"Player {current_symbol} won!")
                game_ongoing = False
            elif is_draw(board):
                print("The game is a draw!")
                game_ongoing = False
            else:
                current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    connect4_game()
