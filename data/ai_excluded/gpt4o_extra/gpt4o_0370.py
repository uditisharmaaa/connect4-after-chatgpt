import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2

# Player checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, columns):
    """Create an empty game board."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_input(col_input):
    """Check if the input column is valid."""
    return col_input.isalpha() and 'A' <= col_input <= chr(ord('A') + COLUMNS - 1)

def place_checker(board, player_checker, column):
    """Place a checker in the board."""
    col = ord(column) - ord('A')
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':  # Find the lowest available space
            board[row][col] = player_checker
            return True
    return False  # Column is full

def check_win(board, player_checker):
    """Check for a win condition."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_checker for i in range(4)):
                return True

    # Check diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == player_checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    """Main function to run the game."""
    board = initialize_board(ROWS, COLUMNS)
    print_board(board)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    while True:
        current_checker = CHECKERS[current_player_index]
        col_input = input(f"Player {current_checker}, please enter a column: ").upper()
        
        if not is_valid_input(col_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        if not place_checker(board, current_checker, col_input):
            print("Column is full. Please choose another column.")
            continue
        
        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break

        # Alternate player turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
