import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYERS = 2  # Set to 2 players as per assignment

def create_board():
    """Creates an empty game board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board."""
    os.system('clear')
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(column, board):
    """Checks if the column input is valid."""
    if len(column) != 1 or not column.isalpha():
        return False
    col_index = ord(column.upper()) - 65
    if col_index < 0 or col_index >= COLUMNS:
        return False
    # Check if column is not full
    return board[0][col_index] == ' '

def place_checker(column, checker, board):
    """Places a player's checker in the correct column."""
    col_index = ord(column.upper()) - 65
    for row in reversed(range(ROWS)):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return

def check_winner(board, checker):
    """Checks if the given player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the board is full."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def connect_four():
    """Main function for the Connect 4 game."""
    # Initialize the board and players
    board = create_board()
    checkers = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    print(f"Player {checkers[current_player]} goes first!")

    while True:
        # Prompt player for input
        print_board(board)
        player_checker = checkers[current_player]
        column = input(f"Player {player_checker}, please enter a column: ")

        # Validate input
        while not is_valid_input(column, board):
            print("Invalid input. Please enter a valid column.")
            column = input(f"Player {player_checker}, please enter a column: ")

        # Place the checker
        place_checker(column, player_checker, board)

        # Check for win
        if check_winner(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    connect_four()
