import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with the specified number of rows and columns."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the terminal
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_valid_input(player):
    """Prompt the player for input until a valid column is entered."""
    while True:
        column = input(f"Player {player}, please enter a column (A-G): ").upper()
        if len(column) == 1 and column >= 'A' and column < chr(65 + COLUMNS):
            return ord(column) - 65  # Convert 'A'-'G' to 0-6
        print("Invalid input. Please try again.")

def place_checker(board, column, checker):
    """Place a checker in the specified column."""
    for row in reversed(board):  # Start from the bottom
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the given checker has won the game."""
    # Check horizontal, vertical, and diagonal lines for a win
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == checker:
                # Check horizontally
                if c + 3 < COLUMNS and all(board[r][c + i] == checker for i in range(4)):
                    return True
                # Check vertically
                if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                    return True
                # Check diagonal down-right
                if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
                # Check diagonal down-left
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    return all(board[r][c] != " " for r in range(ROWS) for c in range(COLUMNS))

def connect4():
    """Main function to run the Connect 4 game."""
    board = create_board()
    players = CHECKERS[:2]  # Set to 2 players
    current_player_index = random.randint(0, len(players) - 1)  # Randomly select first player

    while True:
        print_board(board)
        current_player = players[current_player_index]
        
        # Get and place the checker
        column = get_valid_input(current_player)
        if not place_checker(board, column, current_player):
            print(f"Column {chr(column + 65)} is full. Try again.")
            continue  # Invalid turn, ask for input again

        # Check for win or draw
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Move to the next player
        current_player_index = (current_player_index + 1) % len(players)

# Run the game
if __name__ == "__main__":
    connect4()
