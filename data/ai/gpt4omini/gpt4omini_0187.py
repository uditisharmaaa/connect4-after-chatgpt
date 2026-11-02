import os
import random

# Constants for the game configuration
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def print_board(board):
    """Print the current state of the game board."""
    print("  " + "   ".join(chr(i + 65) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(col_input):
    """Validate the player input for column selection."""
    if len(col_input) != 1 or not col_input.isalpha():
        return False
    col_index = ord(col_input.upper()) - 65
    return 0 <= col_index < COLS

def get_column_index(col_input):
    """Convert column input (A-G) to an index (0-6)."""
    return ord(col_input.upper()) - 65

def drop_checker(board, col, checker):
    """Drop a checker into the specified column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    """Check for a win condition."""
    # Check horizontal, vertical, and diagonal wins
    return (check_horizontal(board, checker) or 
            check_vertical(board, checker) or 
            check_diagonal(board, checker))

def check_horizontal(board, checker):
    """Check horizontal win."""
    for row in board:
        count = 0
        for cell in row:
            count = count + 1 if cell == checker else 0
            if count >= 4:
                return True
    return False

def check_vertical(board, checker):
    """Check vertical win."""
    for col in range(COLS):
        count = 0
        for row in board:
            count = count + 1 if row[col] == checker else 0
            if count >= 4:
                return True
    return False

def check_diagonal(board, checker):
    """Check diagonal win."""
    # Check for positive slope diagonals
    for row in range(ROWS):
        for col in range(COLS):
            if (row <= ROWS - 4 and col <= COLS - 4 and 
                all(board[row+i][col+i] == checker for i in range(4))):
                return True
            # Check for negative slope diagonals
            if (row >= 3 and col <= COLS - 4 and 
                all(board[row-i][col+i] == checker for i in range(4))):
                return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    num_players = min(MAX_PLAYERS, len(CHECKERS))
    players = CHECKERS[:num_players]
    
    # Choose a random first player
    current_player_index = random.randint(0, num_players - 1)
    
    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column (A-G): ")

        while True:
            col_input = input().strip()
            if is_valid_input(col_input):
                col_index = get_column_index(col_input)
                if drop_checker(board, col_index, current_checker):
                    break
                else:
                    print("Column is full! Please try again.")
            else:
                print("Invalid input! Please enter a valid column (A-G).")

        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
