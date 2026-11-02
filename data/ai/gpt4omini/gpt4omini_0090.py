import os
import random

# Constants for the game configuration
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for each player

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current game board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))  # Column labels A to G
    print("+" + "---+" * COLS)  # Separator line
    for row in board:
        print("| " + " | ".join(row) + " |")  # Print each row of the board
        print("+" + "---+" * COLS)  # Separator line

def is_valid_input(column):
    """Check if the input column is valid (A-G)."""
    return len(column) == 1 and column.isalpha() and 'A' <= column <= chr(65 + COLS - 1)

def get_column_index(column):
    """Get the column index from the letter (A-G)."""
    return ord(column) - 65

def can_place_checker(board, column_index):
    """Check if a checker can be placed in the given column."""
    return board[0][column_index] == ' '

def place_checker(board, column_index, checker):
    """Place a checker in the specified column."""
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            return

def check_winner(board, checker):
    """Check if the specified player has won."""
    # Check horizontal, vertical, and diagonal
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal checks
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (board full)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    players = CHECKERS[:2]  # Limit to 2 players for submission
    current_player = random.choice(players)
    turn_index = 0

    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        user_input = input().upper()

        while not is_valid_input(user_input):
            print("Invalid input. Please enter a valid column (A-G):")
            user_input = input().upper()

        column_index = get_column_index(user_input)

        if can_place_checker(board, column_index):
            place_checker(board, column_index, current_player)
            print_board(board)

            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break

            if is_draw(board):
                print("The game is a draw!")
                break

            # Switch players
            turn_index = (turn_index + 1) % len(players)
            current_player = players[turn_index]
        else:
            print("Column is full, try again.")

if __name__ == "__main__":
    main()
