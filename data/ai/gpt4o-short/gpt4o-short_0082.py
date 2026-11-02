import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Maximum of 5 players

# Define the maximum number of players, adjust as needed for the class
MAX_PLAYERS = 5

# Initialize the game board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the console screen
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (COLUMNS * 2 + 1))

# Check if a player has won
def check_win(board, player):
    # Check horizontal, vertical and diagonal for a win (4 in a row)
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
            if all(board[row + 3 - i][col + i] == player for i in range(4)):
                return True

    return False

# Check if the board is full
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Get the column index from the user input
def get_column_index(column_label):
    try:
        return COLUMN_LABELS.index(column_label)
    except ValueError:
        return -1

# Insert a player's piece into a column
def make_move(board, col, player):
    for row in reversed(board):  # Start from the bottom row
        if row[col] == ' ':
            row[col] = player
            return True
    return False

# Main game loop
def play_game(num_players):
    board = create_board()
    current_player = random.choice(PLAYERS[:num_players])  # Choose a random first player
    while True:
        print_board(board)
        print(f"Player {current_player}'s turn.")
        
        # Get and validate user input
        move = input("Choose a column (A-G): ").upper()
        col = get_column_index(move)

        if col == -1 or not make_move(board, col, current_player):
            print("Invalid move. Try again.")
            continue
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Move to the next player
        current_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_index + 1) % num_players]

# Set the number of players for the game
num_players = 2  # You can set this to any number between 2 to MAX_PLAYERS
play_game(num_players)
