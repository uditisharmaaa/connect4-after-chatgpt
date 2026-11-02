import os
import random

# Constants for the game configuration
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
WINNING_COUNT = 4

def create_board():
    """Create and return the Connect 4 board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the console before printing
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers A, B, C, ...
    print("+" + "---+" * COLS)  # Top border
    
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row contents
        print("+" + "---+" * COLS)  # Row border
    print()  # Empty line for readability

def drop_checker(board, column, player):
    """Drop a checker for the specified player into the specified column."""
    for row in reversed(board):  # Start from the bottom of the column
        if row[column] == " ":
            row[column] = player
            return True
    return False  # Column is full

def is_winner(board, player):
    """Check if the specified player has a winning condition."""
    # Check horizontal
    for row in board:
        for col in range(COLS - WINNING_COUNT + 1):
            if all(row[col + i] == player for i in range(WINNING_COUNT)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - WINNING_COUNT + 1):
            if all(board[row + i][col] == player for i in range(WINNING_COUNT)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WINNING_COUNT + 1):
        for col in range(COLS - WINNING_COUNT + 1):
            if all(board[row + i][col + i] == player for i in range(WINNING_COUNT)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(WINNING_COUNT - 1, ROWS):
        for col in range(COLS - WINNING_COUNT + 1):
            if all(board[row - i][col + i] == player for i in range(WINNING_COUNT)):
                return True

    return False

def is_draw(board):
    """Check if the board is full and there's no winner."""
    return all(cell != " " for row in board for cell in row)

def get_valid_input(player):
    """Get a valid column input from the player."""
    while True:
        column = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1):
            col_index = ord(column) - 65
            return col_index
        else:
            print("Invalid input, please try again.")

def main():
    # Initialize game
    board = create_board()
    current_player_index = random.randint(0, len(PLAYER_SYMBOLS) - 1)
    
    # Main game loop
    while True:
        print_board(board)
        current_player = PLAYER_SYMBOLS[current_player_index]

        # Request valid input from the player
        col_index = get_valid_input(current_player)
        if not drop_checker(board, col_index, current_player):
            print("Column is full! Please choose a different column.")
            continue  # Player loses their turn but remains in the game loop

        # Check for win or draw
        if is_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Move to the next player
        current_player_index = (current_player_index + 1) % len(PLAYER_SYMBOLS)

if __name__ == "__main__":
    main()
