import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def create_board():
    """Create the game board as a 2D list initialized with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column_input):
    """Check if the input is a valid column (A-G)."""
    return column_input.isalpha() and 65 <= ord(column_input) <= 65 + COLS - 1

def get_column_index(column_input):
    """Convert the column input (A-G) into an index (0-6)."""
    return ord(column_input) - 65

def place_checker(board, column_index, player_symbol):
    """Place the player's checker in the specified column."""
    for row in reversed(board):  # Check from bottom to top
        if row[column_index] == ' ':
            row[column_index] = player_symbol
            return True  # Checker placed successfully
    return False  # Column is full

def check_win(board, player_symbol):
    """Check for a win condition for the specified player symbol."""
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLS):
            if c + 3 < COLS and all(board[r][c + i] == player_symbol for i in range(4)):
                return True  # Horizontal win
            if r + 3 < ROWS and all(board[r + i][c] == player_symbol for i in range(4)):
                return True  # Vertical win
            if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player_symbol for i in range(4)):
                return True  # Diagonal win (bottom-left to top-right)
            if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == player_symbol for i in range(4)):
                return True  # Diagonal win (top-left to bottom-right)
    return False

def check_draw(board):
    """Check if the board is full and no winner is found."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Initialize game
    board = create_board()
    current_player_index = random.randint(0, min(len(PLAYER_SYMBOLS) - 1, 1))  # Randomly select initial player
    
    while True:
        print_board(board)
        current_player = PLAYER_SYMBOLS[current_player_index]  # Determine current player
        column_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        
        while not is_valid_input(column_input):
            column_input = input("Invalid column. Please enter a valid column (A-G): ").upper()
        
        column_index = get_column_index(column_input)
        
        if place_checker(board, column_index, current_player):
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % len(PLAYER_SYMBOLS)  # Move to the next player
        else:
            print("Column is full! Please choose another column.")

if __name__ == "__main__":
    main()
