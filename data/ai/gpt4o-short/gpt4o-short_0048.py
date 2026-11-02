import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players supported
NUM_PLAYERS = 2  # Change this number from 2 to 5 to add more players

# Ensure we have the correct number of players
PLAYER_SYMBOLS = PLAYER_SYMBOLS[:NUM_PLAYERS]

# Initialize the game board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Display the board
def print_board(board):
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')

# Check if the board is full
def is_board_full(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Check for a win condition
def check_winner(board, symbol):
    # Check horizontal, vertical, and diagonal for a win
    # Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True
    # Vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True
    # Diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True
    # Diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True
    return False

# Place a piece in the board
def place_piece(board, col, symbol):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return True
    return False

# Get the next move from the player
def get_next_move(current_player):
    while True:
        try:
            move = input(f"Player {current_player} ({PLAYER_SYMBOLS[current_player]}), enter a column (A-G): ").upper()
            if move in COLUMN_LABELS:
                return COLUMN_LABELS.index(move)
            else:
                print("Invalid column. Please choose a column from A to G.")
        except ValueError:
            print("Invalid input. Please enter a column from A to G.")

def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        os.system('clear')
        print_board(board)
        
        # Get the next valid move
        col = get_next_move(current_player)

        if not place_piece(board, col, PLAYER_SYMBOLS[current_player]):
            print("Column full. Try again.")
            continue
        
        # Check for victory or draw
        if check_winner(board, PLAYER_SYMBOLS[current_player]):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} ({PLAYER_SYMBOLS[current_player]}) wins!")
            break
        
        if is_board_full(board):
            os.system('clear')
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
