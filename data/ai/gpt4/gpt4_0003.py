import os
import random

# Constants (can be modified)
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Maximum 5 players supported

# Initialize the board
def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear screen
    # Print column labels
    print("  " + "   ".join([chr(65 + i) for i in range(len(board[0]))]))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Drop checker into the chosen column
def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

# Check horizontal, vertical, and diagonal wins
def check_win(board, checker):
    rows, cols = len(board), len(board[0])
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] == checker:
                return True
                
    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] == checker:
                return True
                
    # Check diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] == checker:
                return True
    
    # Check diagonal (top-right to bottom-left)
    for r in range(rows - 3):
        for c in range(3, cols):
            if board[r][c] == board[r + 1][c - 1] == board[r + 2][c - 2] == board[r + 3][c - 3] == checker:
                return True
                
    return False

# Check draw
def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Get a valid column input from the player
def get_valid_column(board, player):
    while True:
        try:
            column_input = input(f"Player {player}, please enter a column: ").strip().upper()
            if len(column_input) != 1 or not column_input.isalpha():
                raise ValueError("Invalid input. Please enter a single letter.")
            
            column = ord(column_input) - 65  # Convert letter to index
            if column < 0 or column >= len(board[0]):
                raise ValueError("Invalid column. Please select a valid column.")

            # Check if column is full
            if board[0][column] != " ":
                raise ValueError("Column is full. Please choose another column.")
            
            return column
        except ValueError as e:
            print(e)

# Main game loop
def connect4():
    # Initialize the game
    board = initialize_board(ROWS, COLUMNS)
    player_count = PLAYERS
    active_players = CHECKERS[:player_count]
    random.shuffle(active_players)
    turn = 0  # Index of the current player
    winner = None

    print_board(board)
    print(f"Player order: {', '.join(active_players)}\n")
    
    while True:
        current_player = active_players[turn]
        column = get_valid_column(board, current_player)
        
        # Drop the checker
        drop_checker(board, column, current_player)
        print_board(board)
        
        # Check for a win
        if check_win(board, current_player):
            winner = current_player
            break
        
        # Check for a draw
        if check_draw(board):
            break
        
        # Next turn
        turn = (turn + 1) % player_count

    # End of game
    if winner:
        print(f"Player {winner} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    connect4()
