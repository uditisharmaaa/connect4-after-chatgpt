import os
import random

# Constants for the game configuration
ROWS = 6  # Number of rows
COLS = 7  # Number of columns
PLAYERS = ["X", "O", "V", "H", "M"]  # Checkers for players, can support up to 5 players

def initialize_board():
    """Create a two-dimensional game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear')  # Clear the terminal screen to show updated board
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels (A, B, C, ...)
    print("+---" + "+---" * (COLS - 1) + "+")  # Print top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Print rows
        print("+---" + "+---" * (COLS - 1) + "+")  # Print borders after each row

def get_valid_input(player):
    """Get and validate column input from the current player."""
    while True:
        column = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if column in [chr(65 + i) for i in range(COLS)]:  # Check if input is a valid column
            return ord(column) - 65  # Return column index
        else:
            print("Invalid input. Please enter a valid column.")

def drop_checker(board, column, checker):
    """Drop a checker into the specified column if possible."""
    for row in reversed(range(ROWS)):  # Check from bottom to top
        if board[row][column] == ' ':
            board[row][column] = checker  # Place the checker
            return True
    return False  # Column is full

def check_winner(board, checker):
    """Check if the specified checker has won the game."""
    # Check horizontal, vertical, and diagonal for 4 connected
    for c in range(COLS):
        for r in range(ROWS):
            # Check horizontal
            if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):
                return True
            # Check vertical
            if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                return True
            # Check diagonal \
            if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):
                return True
            # Check diagonal /
            if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()  # Create the game board
    current_player_index = random.randint(0, len(PLAYERS) - 1)  # Randomly select the first player
    game_active = True

    while game_active:
        print_board(board)  # Print the current game board
        current_player = PLAYERS[current_player_index]  # Get the current player's checker
        column = get_valid_input(current_player)  # Get valid column from player
        
        if drop_checker(board, column, current_player):
            # Check for win after placing the checker
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                game_active = False
            elif check_draw(board):
                print_board(board)
                print("The game is a draw!")
                game_active = False
            else:
                current_player_index = (current_player_index + 1) % len(PLAYERS)  # Switch to the next player
        else:
            print("Column is full! Try a different column.")

if __name__ == "__main__":
    main()  # Run the game
