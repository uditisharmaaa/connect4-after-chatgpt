import os
import random

# Constants for configuration
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board."""
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_column(column, board):
    """Checks if a column choice is valid."""
    if column < 0 or column >= COLS:
        return False
    return board[0][column] == " "

def drop_checker(board, column, checker):
    """Drops a checker into the selected column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    """Checks if the given checker has won."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    
    # Check diagonal (\)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (/)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][c] != " " for c in range(COLS))

def get_column_input():
    """Prompts the player for a valid column input."""
    while True:
        col_input = input("Please enter a column: ").strip()
        if len(col_input) == 1 and col_input.isalpha():
            col_index = ord(col_input.upper()) - 65
            if 0 <= col_index < COLS:
                return col_index
        print("Invalid input. Please enter a letter corresponding to a column.")

def main():
    """Main function to run the Connect 4 game."""
    # Initialize game state
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    clear_screen()
    print_board(board)
    
    while True:
        print(f"Player {CHECKERS[current_player]}'s turn.")
        
        column = get_column_input()
        
        if not is_valid_column(column, board):
            print("Column is full or invalid. Try again.")
            continue
        
        drop_checker(board, column, CHECKERS[current_player])
        clear_screen()
        print_board(board)
        
        # Check for win or draw
        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
