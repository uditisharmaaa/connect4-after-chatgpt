import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def initialize_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column headers
    print("+---" + "+---" * (COLUMNS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLUMNS - 1) + "+")

def is_valid_input(col):
    """Check if the user's input is a valid column."""
    return col in range(COLUMNS)

def place_checker(board, column, checker):
    """Place a checker on the board in the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check for a win condition for the given checker."""
    # Check horizontal, vertical and diagonal (both directions)
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (c + 3 < COLUMNS and all(board[r][c + i] == checker for i in range(4))) or \
               (r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4))) or \
               (r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == checker for i in range(4))) or \
               (r - 3 >= 0 and c + 3 < COLUMNS and all(board[r - i][c + i] == checker for i in range(4))):
                return True
    return False

def check_draw(board):
    """Check if the board is full and the game is a draw."""
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.randint(0, len(PLAYERS) - 1)

    print_board(board)

    while True:
        checker = PLAYERS[current_player]
        print(f"Player {checker}, please enter a column (A-{chr(65 + COLUMNS - 1)}): ", end='')
        user_input = input().upper()
        
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a letter corresponding to a column.")
            continue
        
        column = ord(user_input) - 65
        if not is_valid_input(column):
            print("Invalid column. Please enter a letter corresponding to a column (A-G).")
            continue
        
        if not place_checker(board, column, checker):
            print("Column is full. Please choose another column.")
            continue
        
        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % len(PLAYERS)  # Switch to the next player

if __name__ == "__main__":
    main()
