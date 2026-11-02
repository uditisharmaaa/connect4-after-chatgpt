import os
import random

# Constants for board dimensions and player checkers
BOARD_ROWS = 6
BOARD_COLUMNS = 7
MAX_PLAYERS = 5  # Maximum players supported
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Create a game board with the given rows and columns, initialized with spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    headers = '  '.join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {headers}")
    # Print top edge of board
    print('+---' * len(board[0]) + '+')
    # Print the board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print('+---' * len(board[0]) + '+')

def is_valid_input(column, board):
    """Check if the user input column is valid."""
    return column.isalpha() and 'A' <= column <= chr(64 + len(board[0]))

def is_column_full(column_index, board):
    """Check if a column is already full."""
    return all(row[column_index] != ' ' for row in board)

def place_checker(column_index, board, checker):
    """Place the player's checker in the chosen column."""
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            break

def check_winner(board, checker):
    """Check if the given checker has a winning condition."""
    rows, columns = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(columns - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(columns):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(columns - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, rows):
        for c in range(columns - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (all columns are full)."""
    return all(is_column_full(c, board) for c in range(len(board[0])))

def main():
    """Main Connect 4 game logic."""
    # Creating the board
    board = create_board(BOARD_ROWS, BOARD_COLUMNS)

    # Number of players (can alter as needed)
    num_players = 2
    checkers = PLAYER_CHECKERS[:num_players]

    # Randomly choose the first player
    current_player_index = random.randint(0, num_players - 1)

    clear_screen()
    print_board(board)

    # Main game loop
    while True:
        current_checker = checkers[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        user_input = input().strip().upper()

        # Validate user input
        if not is_valid_input(user_input, board):
            print("Invalid input, please enter a valid column (e.g., A, B, C).")
            continue

        # Convert column letter to index
        column_index = ord(user_input) - 65

        # Check if column is full
        if is_column_full(column_index, board):
            print("Column is full. Choose a different column.")
            continue

        # Place the checker and clear the screen
        place_checker(column_index, board, current_checker)
        clear_screen()
        print_board(board)

        # Check if the current player has won
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check if the game is a draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
