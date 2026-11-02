import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a board initialized with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers
    print("+" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row content
        print("+" + "---+" * COLS)  # Row separator

def is_valid_input(col_input):
    """Check if the user input is a valid column."""
    return col_input in [chr(65 + i) for i in range(COLS)]

def drop_checker(board, column, player):
    """Drop a checker for a player in the specified column, if possible."""
    for row in reversed(range(ROWS)):
        if board[row][column] == ' ':
            board[row][column] = player
            return True
    return False

def check_winner(board, player):
    """Check if the given player has won the game."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
                
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
                
    # Check diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
                
    # Check diagonal (down-left)
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if all(board[r + i][c - i] == player for i in range(4)):
                return True
                
    return False

def is_draw(board):
    """Check if the board is full and there is no winner."""
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        
        if not is_valid_input(col_input):
            print("Invalid input. Please enter a valid column (A-G).")
            continue
            
        column = ord(col_input) - 65  # Convert letter to index
        
        if drop_checker(board, column, current_player):
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print_board(board)
                print("The game is a draw.")
                break
            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full. Please choose another column.")

if __name__ == "__main__":
    main()
