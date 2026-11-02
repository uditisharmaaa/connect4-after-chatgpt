import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates a game board initialized with whitespace."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers A, B, C, ...
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)
        
def get_column_choice(player):
    """Prompts the player for a valid column choice."""
    while True:
        choice = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if len(choice) != 1 or choice not in [chr(65 + i) for i in range(COLS)]:
            print("Invalid input. Please try again.")
        else:
            return ord(choice) - 65  # Convert character to column index

def place_checker(board, column, checker):
    """Places the checker in the specified column if possible."""
    for row in reversed(board):  # Start from the bottom row
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Checks if the specified player has won."""
    # Check horizontal, vertical and diagonal (both directions)
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                # Horizontal
                if c <= COLS - 4 and all(board[r][c + i] == checker for i in range(4)):
                    return True
                # Vertical
                if r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4)):
                    return True
                # Diagonal (top-left to bottom-right)
                if r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
                # Diagonal (bottom-left to top-right)
                if r >= 3 and c <= COLS - 4 and all(board[r - i][c + i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialization
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        column = get_column_choice(current_player)
        
        if place_checker(board, column, current_player):
            print_board(board)  # Show updated board
            
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            if check_draw(board):
                print("The game is a draw!")
                break
            
            current_player_index = (current_player_index + 1) % len(PLAYERS)  # Switch to next player
        else:
            print("Column is full. This turn is lost.")

if __name__ == "__main__":
    main()
