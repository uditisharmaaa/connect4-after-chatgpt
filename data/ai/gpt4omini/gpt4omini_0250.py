import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with specified dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels
    print("+" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Rows
        print("+" + "---+" * COLS)  # Row border

def is_valid_input(column):
    """Check if the input column is valid."""
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1)

def get_column_index(column):
    """Convert column letter to index (0-based)."""
    return ord(column) - 65

def place_checker(board, column, token):
    """Place the player's checker in the chosen column."""
    col_idx = get_column_index(column)
    for row in reversed(board):  # Start from the bottom row
        if row[col_idx] == " ":
            row[col_idx] = token
            return True  # Checker placed
    return False  # Column is full

def check_win(board, token):
    """Check if the current player has won."""
    # Check horizontal, vertical, and diagonal wins
    return (check_horizontal(board, token) or
            check_vertical(board, token) or
            check_diagonal(board, token))

def check_horizontal(board, token):
    """Check for horizontal win for the player."""
    for row in board:
        count = 0
        for cell in row:
            count = count + 1 if cell == token else 0
            if count == 4:
                return True
    return False

def check_vertical(board, token):
    """Check for vertical win for the player."""
    for col in range(COLS):
        count = 0
        for row in range(ROWS):
            count = count + 1 if board[row][col] == token else 0
            if count == 4:
                return True
    return False

def check_diagonal(board, token):
    """Check for diagonal win (both directions) for the player."""
    # Check for diagonals from bottom-left to top-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == token for i in range(4)):
                return True
    
    # Check for diagonals from top-left to bottom-right
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == token for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the board is full without any winner."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main method to run the Connect 4 game."""
    # Initialize the game
    board = create_board()
    num_players = min(len(PLAYER_TOKENS), MAX_PLAYERS)  # Limit to max players
    current_player = random.randint(0, num_players - 1)  # Randomly select first player
    
    # Game loop
    while True:
        print_board(board)
        token = PLAYER_TOKENS[current_player]
        column = input(f"Player {token}, please enter a column: ").strip().upper()
        
        while not is_valid_input(column) or not place_checker(board, column, token):
            if not is_valid_input(column):
                print("Invalid input. Please enter a valid column (A-G).")
            else:
                print("This column is full. Please choose another column.")
            column = input(f"Player {token}, please enter a column: ").strip().upper()
        
        # Check for a win
        if check_win(board, token):
            print_board(board)
            print(f"Player {token} won!")
            break
        
        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
