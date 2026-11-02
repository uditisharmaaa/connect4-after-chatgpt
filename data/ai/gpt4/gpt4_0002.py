import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # 'A', 'B', ..., 'G'

# Function to initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear screen
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Function to find the next available row in a column
def get_next_available_row(board, column):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            return row
    return None

# Function to check for a win
def check_win(board, symbol):
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (c + 3 < COLUMNS and all(board[r][c + i] == symbol for i in range(4))) or \
               (r + 3 < ROWS and all(board[r + i][c] == symbol for i in range(4))) or \
               (r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == symbol for i in range(4))) or \
               (r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == symbol for i in range(4))):
                return True
    return False

# Function to check if the board is full (draw)
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main function to handle the game
def play_game():
    # Initialize the game variables
    board = create_board()
    num_players = 2  # Set to 2, can be changed to any number between 2 and MAX_PLAYERS
    player_symbols = PLAYERS[:num_players]
    current_player = random.choice(player_symbols)  # Randomly select first player
    
    print_board(board)
    
    while True:
        # Player turn
        print(f"Player {current_player}, please enter a column:")
        move = input().upper()

        # Validate input
        if move not in COLUMN_LABELS:
            print("Invalid input. Please enter a valid column letter.")
            continue

        column = COLUMN_LABELS.index(move)
        row = get_next_available_row(board, column)
        if row is None:
            print("Column is full. Please choose another column.")
            continue

        # Place the checker
        board[row][column] = current_player
        print_board(board)

        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = player_symbols.index(current_player)
        current_player = player_symbols[(current_player_index + 1) % num_players]

# Run the game
if __name__ == "__main__":
    play_game()
