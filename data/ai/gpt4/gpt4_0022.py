import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

def clear_screen():
    os.system('clear')

# Create the game board initialized with EMPTY_CELL
def create_board():
    return [[EMPTY_CELL for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)))
    print("+---" * COLS + "+")
    # Print each row of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Get column index from player input
def get_column_index(input_value):
    if len(input_value) == 1 and input_value.isalpha():
        col = ord(input_value.upper()) - 65
        if 0 <= col < COLS:
            return col
    return -1

# Place the checker in the selected column
def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            board[row][col] = checker
            return True
    return False

# Check for a win condition
def is_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    
    return False

# Check for a draw condition
def is_draw(board):
    return all(board[0][col] != EMPTY_CELL for col in range(COLS))

# Run the game
def play_game():
    # Initialize board and players
    board = create_board()
    num_players = 2  # As specified in the assignment
    players = PLAYER_SYMBOLS[:num_players]
    current_player = random.randint(0, num_players - 1)
    
    # Print initial board
    print_board(board)
    
    while True:
        # Current player's turn
        player_symbol = players[current_player]
        print(f"Player {player_symbol}, it's your turn!")
        
        # Get valid input from the player
        while True:
            col_input = input("Please enter a column (A-G): ").strip()
            col = get_column_index(col_input)
            if col == -1:
                print("Invalid input. Please enter a valid column letter.")
            elif not place_checker(board, col, player_symbol):
                print(f"Column {col_input} is full. Choose a different column.")
            else:
                break
        
        # Print the updated board
        print_board(board)
        
        # Check for win or draw
        if is_winner(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % num_players

# Run the game
if __name__ == "__main__":
    play_game()
