import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols for up to 5 players

def initialize_board():
    """Initialize a blank Connect 4 board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board to the console."""
    os.system('clear')  # Clear the screen
    # Print Column Labels (A, B, C, ...)
    print("  " + "   ".join(chr(65 + col) for col in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    # Print Rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_column_input():
    """Prompt user for valid column input."""
    while True:
        column = input("Please enter a column (A-G): ").upper()
        if len(column) == 1 and column.isalpha() and "A" <= column < chr(65 + COLUMNS):
            return ord(column) - 65
        print("Invalid input. Please enter a valid column.")

def place_checker(board, column, checker):
    """Place the checker in the lowest available position in the given column."""
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_winner(board, checker):
    """Check if a player has won with 4 consecutive checkers."""
    # Check Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check Vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check Diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check Diagonal (/)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    """Check if the board is completely filled with no winner."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    """Main game loop."""
    # Initialize game variables
    board = initialize_board()
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player_index = random.randint(0, PLAYERS - 1)  # Randomly select first player

    # Game loop
    while True:
        print_board(board)
        print(f"Player {players[current_player_index]}'s turn.")

        # Get column input and place checker
        while True:
            column = get_column_input()
            if place_checker(board, column, players[current_player_index]):
                break
            print("Column is full. Choose another column.")

        # Check for win
        if check_winner(board, players[current_player_index]):
            print_board(board)
            print(f"Player {players[current_player_index]} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
