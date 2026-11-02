import os
import random

# Constants for game configuration
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
NUM_PLAYERS = 2  # Set this to the desired number of players (2-5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checker pieces for up to 5 players
WIN_COUNT = 4  # Number of checkers in a row required to win

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates and initializes the game board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    print("  " + "   ".join(chr(65 + col) for col in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_column_input(player):
    """Gets a valid column input from the player."""
    while True:
        column = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(column) == 1 and 'A' <= column < chr(65 + COLUMNS):
            return ord(column) - 65  # Convert letter to column index
        else:
            print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, column, checker):
    """Drops the checker into the column if possible. Returns True if successful."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_winner(board, checker):
    """Checks if the given checker has won the game."""
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_COUNT + 1):
            if all(board[row][col + i] == checker for i in range(WIN_COUNT)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_COUNT + 1):
            if all(board[row + i][col] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal checks (/ direction)
    for row in range(ROWS - WIN_COUNT + 1):
        for col in range(COLUMNS - WIN_COUNT + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal checks (\ direction)
    for row in range(WIN_COUNT - 1, ROWS):
        for col in range(COLUMNS - WIN_COUNT + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    """Main game logic."""
    # Initialize the board and players
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    # Game loop
    clear_screen()
    print_board(board)
    while True:
        print(f"\nIt's {current_player}'s turn!")
        column = get_column_input(current_player)

        if drop_checker(board, column, current_player):
            clear_screen()
            print_board(board)

            # Check for win or draw
            if check_winner(board, current_player):
                print(f"\nPlayer {current_player} won!")
                break
            if is_draw(board):
                print("\nThe game is a draw!")
                break

            # Switch to next player
            current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]
        else:
            print("Column is full. Try another column.")

if __name__ == "__main__":
    main()
