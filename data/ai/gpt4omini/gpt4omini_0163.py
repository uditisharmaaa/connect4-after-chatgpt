import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board for Connect 4."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Print each row
        print("+" + "---+" * COLS)  # Row border

def get_column_choice(player):
    """Get and validate column input from the current player."""
    while True:
        choice = input(f"Player {player}, please enter a column (A-G): ").upper()
        if len(choice) == 1 and 'A' <= choice <= 'G':
            column_index = ord(choice) - 65
            return column_index
        print("Invalid input. Please enter a valid column (A-G).")

def place_checker(board, column, player):
    """Place a checker for the player in the specified column."""
    for row in reversed(board):  # Check from bottom to top
        if row[column] == " ":
            row[column] = player
            return True
    return False  # Column is full

def check_winner(board, player):
    """Check if the current player has won."""
    # Check horizontal, vertical, and diagonal
    return (check_horizontal(board, player) or
            check_vertical(board, player) or
            check_diagonal(board, player))

def check_horizontal(board, player):
    """Check for horizontal wins."""
    for row in board:
        count = 0
        for cell in row:
            count = count + 1 if cell == player else 0
            if count >= 4:
                return True
    return False

def check_vertical(board, player):
    """Check for vertical wins."""
    for col in range(COLS):
        count = 0
        for row in range(ROWS):
            count = count + 1 if board[row][col] == player else 0
            if count >= 4:
                return True
    return False

def check_diagonal(board, player):
    """Check for diagonal wins (both directions)."""
    # Checking for \ diagonal
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Checking for / diagonal
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    """Check for draw (full board)."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main game loop."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        
        column = get_column_choice(current_player)
        if not place_checker(board, column, current_player):
            print("Column is full! Please select another column.")
            continue  # Turn continues without incrementing player index
        
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
