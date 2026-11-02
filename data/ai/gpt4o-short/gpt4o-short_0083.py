import random
import os

# Constants for player symbols and board dimensions.
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Set the number of players between 2 and 5.
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Function to clear the console screen.
def clear_screen():
    os.system('clear')

# Initialize the board with empty spaces.
def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Display the current state of the board.
def display_board(board):
    clear_screen()
    print('  ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print(' ' + '-' * (2 * COLUMNS + 1))

# Get input from the current player and validate it.
def get_player_input(player):
    while True:
        try:
            choice = input(f"Player {player} ({PLAYER_SYMBOLS[player]}), choose a column (A-G): ").upper()
            if choice in COLUMN_LABELS:
                col_index = COLUMN_LABELS.index(choice)
                if board[0][col_index] == ' ':
                    return col_index
                else:
                    print("Column is full, choose another one.")
            else:
                print("Invalid input. Please choose a column from A to G.")
        except Exception as e:
            print(f"Error: {e}, please try again.")

# Place the player's symbol in the chosen column.
def place_player_symbol(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = PLAYER_SYMBOLS[player]
            break

# Check for a win condition.
def check_win(board, player):
    player_symbol = PLAYER_SYMBOLS[player]
    # Check horizontal, vertical and diagonal lines for a winning streak of 4.
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (col <= COLUMNS-4 and all(board[row][c] == player_symbol for c in range(col, col+4))) or \
               (row <= ROWS-4 and all(board[r][col] == player_symbol for r in range(row, row+4))) or \
               (row <= ROWS-4 and col <= COLUMNS-4 and all(board[row+i][col+i] == player_symbol for i in range(4))) or \
               (row >= 3 and col <= COLUMNS-4 and all(board[row-i][col+i] == player_symbol for i in range(4))):
                return True
    return False

# Check for a draw condition.
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Game loop.
def play_game():
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        display_board(board)
        col_choice = get_player_input(current_player)
        place_player_symbol(board, col_choice, current_player)
        
        if check_win(board, current_player):
            display_board(board)
            print(f"Player {current_player} ({PLAYER_SYMBOLS[current_player]}) wins!")
            break
        elif check_draw(board):
            display_board(board)
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

# Run the game.
play_game()
