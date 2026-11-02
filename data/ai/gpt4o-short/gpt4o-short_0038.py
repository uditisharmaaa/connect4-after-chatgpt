import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Set number of players (between 2 to 5)
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Function to initialize the game board
def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to display the board
def display_board(board):
    os.system('clear')
    print(' '.join(COLUMN_LABELS))
    for row in board:
        print(' '.join(row))
    print()

# Function to pick a random first player
def pick_random_player():
    return random.randint(0, NUM_PLAYERS - 1)

# Function to validate input
def validate_input(column_input):
    return column_input in COLUMN_LABELS

# Function to place a piece on the board
def place_piece(board, column, player_symbol):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player_symbol
            return True
    return False

# Function to check for a win
def check_win(board, player_symbol):
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLUMNS):
            if col <= COLUMNS - 4 and all(board[row][col+i] == player_symbol for i in range(4)):
                return True
            if row <= ROWS - 4 and all(board[row+i][col] == player_symbol for i in range(4)):
                return True
            if row <= ROWS - 4 and col <= COLUMNS - 4 and all(board[row+i][col+i] == player_symbol for i in range(4)):
                return True
            if row >= 3 and col <= COLUMNS - 4 and all(board[row-i][col+i] == player_symbol for i in range(4)):
                return True
    return False

# Function to check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def connect_four():
    board = initialize_board()
    current_player_index = pick_random_player()
    
    while True:
        display_board(board)
        current_player_symbol = PLAYER_SYMBOLS[current_player_index]

        # Get and validate input
        column_input = input(f"Player {current_player_symbol}, choose a column (A-G): ").strip().upper()
        if not validate_input(column_input):
            print("Invalid input. Please choose a column labeled A-G.")
            continue

        # Place the piece
        column_index = COLUMN_LABELS.index(column_input)
        if not place_piece(board, column_index, current_player_symbol):
            print("Column is full. Please choose another column.")
            continue

        # Check for win
        if check_win(board, current_player_symbol):
            display_board(board)
            print(f"Player {current_player_symbol} wins!")
            break
        
        # Check for draw
        if check_draw(board):
            display_board(board)
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == '__main__':
    connect_four()
