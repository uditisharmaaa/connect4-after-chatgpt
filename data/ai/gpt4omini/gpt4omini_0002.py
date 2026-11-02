import os
import random

# Constants for the board dimensions and player characters
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def initialize_board():
    """Create and return a new game board filled with whitespace."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear')  # Clear the terminal for a clean look
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    # Print each row in reverse order (bottom to top)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(column_input, board):
    """Check if the input for the column is valid."""
    if len(column_input) != 1:  # Must be a single character
        return False
    if not column_input.isalpha():  # Must be an alphabet character
        return False
    column_index = ord(column_input.upper()) - 65  # Convert from letter to index
    if column_index < 0 or column_index >= COLUMNS:  # Must be within column limits
        return False
    return board[0][column_index] == " "  # Must not be filled

def place_checker(board, column, checker):
    """Place a checker's token in the specified column."""
    column_index = ord(column.upper()) - 65
    for row in reversed(board):  # Start from the bottom
        if row[column_index] == " ":
            row[column_index] = checker  # Place checker
            return True
    return False  # Column was full

def check_winner(board):
    """Check if there is a winner in the board."""
    for r in range(ROWS):
        for c in range(COLUMNS):
            checker = board[r][c]
            if checker == " ":
                continue  # Skip empty spaces
            
            # Check horizontal
            if c + 3 < COLUMNS and all(board[r][c + i] == checker for i in range(4)):
                return checker
            
            # Check vertical
            if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                return checker
            
            # Check diagonal (down-right)
            if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == checker for i in range(4)):
                return checker
            
            # Check diagonal (down-left)
            if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4)):
                return checker
                
    return None  # No winner

def is_draw(board):
    """Check if the board is full and there is no winner."""
    return all(board[0][c] != " " for c in range(COLUMNS)) and check_winner(board) is None

def main():
    board = initialize_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)  # Randomly select the first player
    game_over = False

    while not game_over:
        print_board(board)
        current_checker = PLAYERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")

        while True:
            column_input = input().strip()  # Get user input for the column
            if is_valid_input(column_input, board):
                place_checker(board, column_input, current_checker)
                break  # Valid input, exit while loop
            else:
                print("Invalid input. Please try again.")

        # Check for a winner
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Player {winner} won!")
            game_over = True
            break

        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
            break
        
        # Move to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
