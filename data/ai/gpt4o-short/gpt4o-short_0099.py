import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change this value to set the number of players (2 to 5)

# Function to clear the terminal screen
def clear_screen():
    os.system('clear')

# Function to initialize the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to display the board
def display_board(board):
    clear_screen()
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (2 * COLUMNS + 1))

# Function to validate user input
def validate_input(input_column, board):
    if input_column in COLUMN_LABELS:
        column_index = COLUMN_LABELS.index(input_column)
        if board[0][column_index] == ' ':  # Check if column is not full
            return column_index
    return None

# Function to make a move
def make_move(board, column_index, symbol):
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = symbol
            break

# Function to check for a win
def check_winner(board, symbol):
    # Check horizontal locations
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == symbol for i in range(4)):
                return True

    # Check vertical locations
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == symbol for i in range(4)):
                return True

    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == symbol for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == symbol for i in range(4)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    board = create_board()
    current_players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(current_players)

    while True:
        display_board(board)
        print(f"Player {current_player}'s turn. Choose a column (A-G):")
        while True:
            user_input = input().strip().upper()
            column_index = validate_input(user_input, board)
            if column_index is not None:
                break
            print("Invalid input. Please choose a valid column (A-G):")

        make_move(board, column_index, current_player)

        if check_winner(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            break
        
        if check_draw(board):
            display_board(board)
            print("It's a draw!")
            break
        
        current_player = current_players[(current_players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
