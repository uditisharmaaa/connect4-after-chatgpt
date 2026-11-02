import os
import random

# Constants for the board dimensions and number of players
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Maximum 5 players supported, as per instructions

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates and initializes the game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the game board."""
    # Print column headers
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(COLS))  # A, B, C...
    print(column_labels)
    print("+---" * COLS + "+")
    
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(column_letter):
    """Checks if the input column is valid."""
    return column_letter.isalpha() and "A" <= column_letter <= chr(65 + COLS - 1)

def get_column_index(column_letter):
    """Converts a column letter (A, B, ...) to a column index (0, 1, ...)."""
    return ord(column_letter) - 65

def drop_checker(board, column, checker):
    """Drops a checker into the specified column."""
    for row in reversed(board):  # Start checking from the bottom row
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

def check_winner(board):
    """Checks the board for a winner (4 in a row in any direction)."""
    # Check horizontal lines
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] != " ":
                return True

    # Check vertical lines
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] != " ":
                return True

    # Check diagonals (/)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] != " ":
                return True

    # Check diagonals (\)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] != " ":
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw (no empty spaces)."""
    return all(cell != " " for row in board for cell in row)

def get_player_input(board, current_player):
    """Gets valid column input from the player."""
    while True:
        column_letter = input(f"Player {current_player}, please enter a column: ").upper()
        if not is_valid_column(column_letter):
            print("Invalid input. Please enter a valid column (e.g., A, B, C, etc.).")
            continue

        column_index = get_column_index(column_letter)
        if board[0][column_index] != " ":
            print(f"Column {column_letter} is full. Please choose another column.")
            continue

        return column_index

def main():
    # Initialize game
    board = create_board()
    num_players = PLAYERS
    player_checkers = CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    clear_screen()
    print_board(board)
    
    # Game loop
    while True:
        current_checker = player_checkers[current_player_index]
        print(f"\nIt's Player {current_checker}'s turn.")
        column = get_player_input(board, current_checker)

        # Drop the checker
        drop_checker(board, column, current_checker)
        clear_screen()
        print_board(board)

        # Check for win or draw
        if check_winner(board):
            print(f"Player {current_checker} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Move to the next player's turn
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
