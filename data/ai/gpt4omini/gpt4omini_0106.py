import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Extendable for up to 5 players

def clear_screen():
    """Clear the console for a cleaner output."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    """Create a 2D board initialized with spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    clear_screen()  # Clear the screen before printing
    # Print column headers
    columns = "   " + "   ".join(chr(65 + i) for i in range(COLS))  # A, B, C, D, E, F, G
    print(columns)
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

def is_valid_input(col_input):
    """Check whether the input is a valid column (A-G)."""
    return col_input.isalpha() and 'A' <= col_input <= chr(65 + COLS - 1)

def get_column_index(col_input):
    """Convert column letter to index."""
    return ord(col_input) - 65

def place_checker(board, column, checker):
    """Place a checker in the specified column."""
    for row in reversed(board):  # Start from the bottom row
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check for a win condition for the specified checker."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check if the board is full (draw condition)."""
    return all(board[0][c] != " " for c in range(COLS))

def main():
    """Main function to execute the game logic."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    # Game loop
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column: ").upper()

        # Validate input
        while not is_valid_input(col_input) or not place_checker(board, get_column_index(col_input), current_player):
            if not is_valid_input(col_input):
                print("Invalid input. Please enter a letter between A and G.")
            else:
                print("Column is full. Please choose another column.")
            col_input = input(f"Player {current_player}, please enter a column: ").upper()
        
        # Check for win or draw
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Move to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
