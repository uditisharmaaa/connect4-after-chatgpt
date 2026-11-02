import os
import random

# Define constants for the game configuration
NUM_ROWS = 6
NUM_COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Set this to any value between 2 and 5

# Ensure NUM_PLAYERS is within the allowed range
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5."

# Initialize the board as a list of lists
board = [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def print_board():
    os.system('clear')  # Clear the console
    # Print column labels
    print(' '.join(COLUMN_LABELS))
    # Print each row of the board
    for row in board:
        print(' '.join(row))

def make_move(player_token):
    while True:
        # Ask for player's input
        column_input = input(f"Player {player_token}, choose a column (A-G): ").upper()
        # Validate input
        if column_input not in COLUMN_LABELS:
            print("Invalid input. Please choose a column labeled A-G.")
            continue

        column_index = COLUMN_LABELS.index(column_input)
        
        # Find the next available row in the selected column
        for row in reversed(board):
            if row[column_index] == ' ':
                row[column_index] = player_token
                return
        print(f"Column {column_input} is full. Choose another column.")

def check_winner():
    # Check for a win condition (4 in a row horizontally, vertically, diagonally)
    def check_line(line):
        for i in range(len(line) - 3):
            if line[i] != ' ' and line[i] == line[i+1] == line[i+2] == line[i+3]:
                return True
        return False

    # Check horizontal lines
    for row in board:
        if check_line(row):
            return True
    
    # Check vertical lines
    for col in range(NUM_COLUMNS):
        column = [board[row][col] for row in range(NUM_ROWS)]
        if check_line(column):
            return True
    
    # Check diagonal lines (bottom-left to top-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if board[row][col] != ' ' and board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                return True

    # Check diagonal lines (top-left to bottom-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if board[row][col] != ' ' and board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]:
                return True

    return False

def check_draw():
    # If all rows are filled and no winner, game is a draw
    return all(board[row][col] != ' ' for row in range(NUM_ROWS) for col in range(NUM_COLUMNS))

def play_game():
    # Choose a random first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        # Print the board state
        print_board()
        # Current player's turn
        make_move(PLAYER_TOKENS[current_player_index])
        
        # Check for win condition
        if check_winner():
            print_board()
            print(f"Player {PLAYER_TOKENS[current_player_index]} wins!")
            break
        
        # Check for draw condition
        if check_draw():
            print_board()
            print("The game is a draw!")
            break
        
        # Switch to next player (circular rotation)
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
play_game()
