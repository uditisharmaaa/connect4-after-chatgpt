import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def create_board(rows, cols):
    """Creates an empty game board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    os.system('clear')  # Clear the terminal screen
    # Print column labels
    column_labels = "   ".join(ALPHABET[:len(board[0])])
    print(f"  {column_labels}")
    print("+" + "---+" * len(board[0]))
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def is_valid_input(input_str, cols):
    """Checks if the user input is valid."""
    return len(input_str) == 1 and input_str in ALPHABET[:cols]

def place_checker(board, col, checker):
    """Places the checker in the specified column if possible."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Checks if a player has won."""
    for r in range(ROWS):
        for c in range(COLUMNS):

            # Horizontal Check
            if c <= COLUMNS - 4 and all(board[r][c + i] == checker for i in range(4)):
                return True

            # Vertical Check
            if r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4)):
                return True

            # Diagonal (\) Check
            if r <= ROWS - 4 and c <= COLUMNS - 4 and all(board[r + i][c + i] == checker for i in range(4)):
                return True

            # Diagonal (/) Check
            if r <= ROWS - 4 and c >= 3 and all(board[r + i][c - i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the board is full (draw)."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize the board
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Start the game
    print_board(board)
    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        
        user_input = input().upper()
        
        # Validate input
        if not is_valid_input(user_input, COLUMNS):
            print("Invalid input. Try again.")
            continue

        column_index = ALPHABET.index(user_input)

        # Try to place the checker
        if not place_checker(board, column_index, current_player):
            print("Column is full! Try another column.")
            continue

        # Print the updated board
        print_board(board)

        # Check for a win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
