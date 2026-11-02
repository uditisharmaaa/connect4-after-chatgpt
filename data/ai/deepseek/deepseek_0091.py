import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]  # Tokens for up to 5 players

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Clear the screen before printing
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    
    # Print the board with borders
    border = "+---" * COLUMNS + "+"
    for row in board:
        print(border)
        print("| " + " | ".join(row) + " |")
    print(border)

def get_valid_column(board, player):
    """Get a valid column input from the player."""
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if len(column) != 1 or not column.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        
        col_index = ord(column) - ord('A')
        if col_index < 0 or col_index >= COLUMNS:
            print(f"Column must be between A and {chr(ord('A') + COLUMNS - 1)}.")
            continue
        
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index

def place_checker(board, col_index, player):
    """Place the player's checker in the lowest available row of the column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player
            return

def check_win(board, player):
    """Check if the player has won the game (horizontally, vertically, diagonally)."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if (board[row][col] == player and 
                board[row][col+1] == player and 
                board[row][col+2] == player and 
                board[row][col+3] == player):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if (board[row][col] == player and 
                board[row+1][col] == player and 
                board[row+2][col] == player and 
                board[row+3][col] == player):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if (board[row][col] == player and 
                board[row+1][col+1] == player and 
                board[row+2][col+2] == player and 
                board[row+3][col+3] == player):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if (board[row][col] == player and 
                board[row-1][col+1] == player and 
                board[row-2][col+2] == player and 
                board[row-3][col+3] == player):
                return True
    
    return False

def check_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    current_player = PLAYER_TOKENS[current_player_index]
    
    while True:
        print_board(board)
        col_index = get_valid_column(board, current_player)
        place_checker(board, col_index, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % PLAYERS
        current_player = PLAYER_TOKENS[current_player_index]

if __name__ == "__main__":
    play_game()
