import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]  # Players' checkers, supports up to 5 players
NUM_PLAYERS = 2  # Changeable to support up to MAX_PLAYERS

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Create an empty board with given rows and columns."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the Connect 4 board to the screen."""
    clear_screen()
    # Print column labels
    column_labels = "  " + "   ".join([chr(65 + i) for i in range(len(board[0]))])
    print(column_labels)
    print("+---" * len(board[0]) + "+")
    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def get_column_index(column_input, columns):
    """Convert column letter input to column index, validating the input."""
    if len(column_input) != 1 or not column_input.isalpha():
        return -1
    column_index = ord(column_input.upper()) - ord('A')
    if 0 <= column_index < columns:
        return column_index
    return -1

def is_column_full(board, column_index):
    """Check if the given column is completely filled."""
    return board[0][column_index] != " "

def place_checker(board, column_index, player_checker):
    """Place a checker in the selected column for the current player."""
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom row
        if board[row][column_index] == " ":
            board[row][column_index] = player_checker
            return True
    return False

def check_win(board, player_checker):
    """Check if the current player has won."""
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

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is completely filled."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    """Main function to run the Connect 4 game."""
    # Create game board
    board = create_board(ROWS, COLUMNS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player = PLAYERS[current_player_index]

    # Game loop
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")

        # Get valid column input
        while True:
            column_input = input().strip()
            column_index = get_column_index(column_input, COLUMNS)
            if column_index == -1:
                print("Invalid input. Please enter a valid column (A-G).")
            elif is_column_full(board, column_index):
                print("Column is full. Please choose another column.")
            else:
                break

        # Place the checker
        place_checker(board, column_index, current_player)

        # Check for a win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_player = PLAYERS[current_player_index]

if __name__ == "__main__":
    main()
