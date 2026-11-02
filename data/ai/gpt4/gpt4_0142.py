import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Initialize board
def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    # Print board rows
    for row in board:
        print("+---" * len(board[0]) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

# Validate column input
def validate_column_input(column, board):
    if len(column) != 1 or not column.isalpha():
        return False
    col_index = ord(column.upper()) - 65
    return 0 <= col_index < len(board[0]) and board[0][col_index] == " "

# Place checker
def place_checker(column, board, symbol):
    col_index = ord(column.upper()) - 65
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            break

# Check for a win
def check_win(board, symbol):
    rows, cols = len(board), len(board[0])
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == symbol for i in range(4)):
                return True
    
    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == symbol for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == symbol for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == symbol for i in range(4)):
                return True
    
    return False

# Check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game logic
def play_game():
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Player setup
    num_players = 2  # Fixed in assignment
    players = PLAYER_SYMBOLS[:num_players]
    current_player = random.choice(players)
    
    print_board(board)
    print(f"Player {current_player} starts!")
    
    while True:
        # Player turn
        print_board(board)
        column = input(f"Player {current_player}, please enter a column: ").strip()
        
        # Validate input
        while not validate_column_input(column, board):
            column = input("Invalid input. Please enter a valid column: ").strip()
        
        # Place the checker
        place_checker(column, board, current_player)
        
        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch player
        current_index = players.index(current_player)
        current_player = players[(current_index + 1) % num_players]

# Run the game
if __name__ == "__main__":
    play_game()
