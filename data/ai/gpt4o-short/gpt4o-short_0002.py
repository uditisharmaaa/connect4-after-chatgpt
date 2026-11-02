import os
import random

# Constants to define game settings
NUM_ROWS = 6
NUM_COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Represents up to 5 players
NUM_PLAYERS = 2  # Change this value between 2 and 5 to have more players

# Function to initialize the game board
def init_board():
    return [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

# Function to display the board
def display_board(board):
    os.system('clear')  # Clear console
    print(' '.join(COLUMN_LABELS))
    for row in board:
        print(' '.join(row))

# Function to validate the input
def is_valid_move(board, move):
    if move not in COLUMN_LABELS:
        return False
    column_index = COLUMN_LABELS.index(move)
    return board[0][column_index] == ' '

# Function to make a move on the board
def make_move(board, column_index, token):
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = token
            break

# Function to check for a victory condition
def check_win(board, token):
    # Check horizontal win
    for row in board:
        for col in range(NUM_COLUMNS - 3):
            if all(s == token for s in row[col:col + 4]):
                return True
    
    # Check vertical win
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if all(board[row + i][col] == token for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right) win
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row + i][col + i] == token for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right) win
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row - i][col + i] == token for i in range(4)):
                return True

    return False

# Function to check for a draw condition
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(NUM_COLUMNS))

# Main game function
def play_game():
    board = init_board()
    current_player = random.choice(range(NUM_PLAYERS))
    while True:
        display_board(board)
        current_token = PLAYER_TOKENS[current_player]
        move = input(f"Player {current_token}, choose a column (A-G): ").strip().upper()
        
        if not is_valid_move(board, move):
            print("Invalid move! Try again.")
            continue
        
        column_index = COLUMN_LABELS.index(move)
        make_move(board, column_index, current_token)

        if check_win(board, current_token):
            display_board(board)
            print(f"Player {current_token} wins!")
            break
        
        if check_draw(board):
            display_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS  # Move to next player

# Start the game
if __name__ == "__main__":
    play_game()
