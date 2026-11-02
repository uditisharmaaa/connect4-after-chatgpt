import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLUMNS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
COLUMN_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Initialize the board
def create_board():
    return [[' ' for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(COLUMN_LETTERS[:BOARD_COLUMNS]))
    print('+---' * BOARD_COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(' ' + cell + ' ' for cell in row) + '|')
        print('+---' * BOARD_COLUMNS + '+')

# Check for a win condition
def check_win(board, player_symbol):
    # Horizontal check
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if all(board[row][col + i] == player_symbol for i in range(4)):
                return True
    
    # Vertical check
    for col in range(BOARD_COLUMNS):
        for row in range(BOARD_ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right) check
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True

    # Diagonal (bottom-left to top-right) check
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(BOARD_COLUMNS))

# Place checker in the board
def place_checker(board, column, player_symbol):
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player_symbol
            return True
    return False

# Get player input
def get_player_input(current_player):
    while True:
        column_letter = input(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column: ").strip().upper()
        if column_letter in COLUMN_LETTERS[:BOARD_COLUMNS]:
            column_index = COLUMN_LETTERS.index(column_letter)
            if place_checker(board, column_index, PLAYER_SYMBOLS[current_player]):
                return column_index
        print("Invalid input. Try again.")

# Main game loop
def connect_four_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        get_player_input(current_player)
        print_board(board)

        if check_win(board, PLAYER_SYMBOLS[current_player]):
            print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

# Start the game
connect_four_game()
