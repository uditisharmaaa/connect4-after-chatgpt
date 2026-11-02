import os
import random

# Constants for board dimensions and the number of players
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    """Create a board with given rows and columns initialized with whitespace."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clears the terminal screen for better visibility
    print("  " + "   ".join(chr(65 + col) for col in range(len(board[0]))))  # Column headers
    print("+" + "---+" * len(board[0]))  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row contents
        print("+" + "---+" * len(board[0]))  # Row separator

def get_column_input(current_player):
    """Prompt the current player for input until a valid column is provided."""
    while True:
        column = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLUMNS - 1)}): ").upper()
        if len(column) == 1 and 'A' <= column <= chr(65 + COLUMNS - 1):
            return ord(column) - 65  # Convert A-G to 0-6
        print("Invalid input. Please try again.")

def place_checker(board, column, checker):
    """Place the checker in the specified column on the board."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check for a win condition for the specified checker."""
    # Check horizontal, vertical, and diagonal connections for wins
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == checker:
                # Check horizontally
                if col + 3 < COLUMNS and all(board[row][col + i] == checker for i in range(4)):
                    return True
                # Check vertically
                if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
                    return True
                # Check diagonally (bottom-right)
                if row + 3 < ROWS and col + 3 < COLUMNS and all(board[row + i][col + i] == checker for i in range(4)):
                    return True
                # Check diagonally (bottom-left)
                if row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Check if the board is full (draw condition)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(ROWS, COLUMNS)  # Create the game board
    current_player_index = random.randint(0, min(len(PLAYERS) - 1, 1))  # Randomly select first player
    total_turns = 0  # Track total turns played

    while True:
        print_board(board)  # Show the current state of the board
        current_player = PLAYERS[current_player_index]  # Get the current player
        column = get_column_input(current_player)  # Get the column input

        if not place_checker(board, column, current_player):
            print("Column is full. Turn lost.")
        else:
            total_turns += 1  # Increment turn count
            # Check for a win
            if check_win(board, current_player):
                print_board(board)  # Print the board one last time
                print(f"Player {current_player} won!")
                break
            # Check for draw
            if total_turns >= ROWS * COLUMNS:
                print_board(board)  # Print the board one last time
                print("The game ended in a draw.")
                break

        # Switch to next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()  # Start the game
