import os
import random

# Constants for board dimensions and player checkers
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def initialize_board():
    """Create a 2D list representing the Connect 4 board initialized with spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the terminal for better visibility
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Print column headers
    print("+---+" + "---+" * (COLS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1))

def is_valid_input(col_str):
    """Validate the user's column input."""
    if len(col_str) == 1 and col_str.isalpha():
        col_index = ord(col_str.upper()) - 65
        return 0 <= col_index < COLS
    return False

def get_column_input(player):
    """Prompt the player for a valid column input."""
    while True:
        col_str = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ")
        if is_valid_input(col_str):
            return ord(col_str.upper()) - 65  # Convert column letter to index
        print("Invalid input. Please try again.")

def place_checker(board, col, checker):
    """Place the checker's piece in the specified column."""
    for row in reversed(board):  # Start from the bottom
        if row[col] == " ":
            row[col] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the specified checker has a winning condition."""
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLS):
            if (
                check_direction(board, row, col, 1, 0, checker) or  # Horizontal
                check_direction(board, row, col, 0, 1, checker) or  # Vertical
                check_direction(board, row, col, 1, 1, checker) or  # Diagonal \
                check_direction(board, row, col, 1, -1, checker)    # Diagonal /
            ):
                return True
    return False

def check_direction(board, row, col, delta_row, delta_col, checker):
    """Check for four in a row in a specified direction."""
    count = 0
    for i in range(4):  # Check for four in a row
        r, c = row + i * delta_row, col + i * delta_col
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
        else:
            break
    return count == 4

def check_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.randint(0, len(PLAYERS) - 1)  # Randomly select first player
    
    print_board(board)
    
    while True:
        player_checker = PLAYERS[current_player]
        col = get_column_input(player_checker)
        
        if not place_checker(board, col, player_checker):
            print("Column is full. Please try another column.")
            continue  # Skip to next player if column is full
        
        print_board(board)  # Show the updated board
        
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % len(PLAYERS)  # Switch to the next player

if __name__ == "__main__":
    main()
