import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Initialize the game board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the screen
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))  # A, B, C, etc.
    print(column_labels)
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

# Validate user input
def is_valid_move(input_col, board):
    if len(input_col) != 1 or not input_col.isalpha():
        return False
    
    col_index = ord(input_col.upper()) - 65
    if col_index < 0 or col_index >= len(board[0]):
        return False
    
    return board[0][col_index] == " "

# Place a token on the board
def place_checker(board, col, symbol):
    col_index = ord(col.upper()) - 65
    for row in reversed(board):  # Start from the bottom of the column
        if row[col_index] == " ":
            row[col_index] = symbol
            break

# Check if a player has won
def is_winner(board, symbol):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col:col + 4] == [symbol] * 4:
                return True
    
    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True
    
    # Check diagonal (\)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True
    
    # Check diagonal (/)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

# Check if the game is a draw
def is_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game loop
def play_game():
    # Initialize game
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Fixed at 2 players for this assignment
    player_symbols = PLAYER_SYMBOLS[:num_players]
    current_player = random.randint(0, num_players - 1)
    
    print_board(board)
    print(f"Randomly selected Player {player_symbols[current_player]} starts!")
    
    while True:
        # Prompt the current player for input
        current_symbol = player_symbols[current_player]
        user_input = input(f"Player {current_symbol}, please enter a column (A-{chr(65 + COLUMNS - 1)}): ")
        
        # Validate input
        if not is_valid_move(user_input, board):
            print("Invalid input. Please try again.")
            continue
        
        # Place the checker and update the board
        place_checker(board, user_input, current_symbol)
        print_board(board)
        
        # Check for a win
        if is_winner(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break
        
        # Check for a draw
        if is_draw(board):
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % num_players

# Start the game
if __name__ == "__main__":
    play_game()
