import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Checkers for 2 to 5 players

def create_board():
    """Create a 2D board initialized with spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(i) for i in range(ord('A'), ord('A') + COLS)))  # Column labels
    print("+---" * COLS + "+")  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row content
        print("+---" * COLS + "+")  # Row border

def is_valid_input(col):
    """Check if the input column is valid (A-G)."""
    return col in range(COLS)

def get_lowest_empty_row(board, col):
    """Return the lowest empty row in the specified column, or None if the column is full."""
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            return row
    return None

def place_checker(board, col, checker):
    """Place the checker in the specified column if there is space."""
    row = get_lowest_empty_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True
    return False

def check_win(board, checker):
    """Check if the specified player has won the game."""
    # Check horizontal, vertical, and diagonal directions
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                # Check horizontal
                if col + 3 < COLS and all(board[row][col + i] == checker for i in range(4)):
                    return True
                # Check vertical
                if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
                    return True
                # Check diagonal down-right
                if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == checker for i in range(4)):
                    return True
                # Check diagonal down-left
                if row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Check if the board is full without any winners (draw scenario)."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    """Main function to control the game flow."""
    board = create_board()
    current_player = random.randint(0, len(PLAYERS) - 1)

    print_board(board)

    while True:
        checker = PLAYERS[current_player]
        print(f"Player {checker}, please enter a column (A-G):")
        
        while True:
            user_input = input().strip().upper()
            if len(user_input) == 1 and user_input >= 'A' and user_input <= chr(ord('A') + COLS - 1):
                col = ord(user_input) - ord('A')
                if is_valid_input(col):
                    if place_checker(board, col, checker):
                        break
                    else:
                        print("Column is full, choose another column.")
                else:
                    print("Invalid column. Please choose again.")
            else:
                print("Invalid input. Enter a letter between A and G.")

        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % len(PLAYERS)

# Run the game
if __name__ == "__main__":
    main()
