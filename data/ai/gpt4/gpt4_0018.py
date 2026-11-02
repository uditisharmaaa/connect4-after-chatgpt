import os
import random

# Constants for game settings
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"][:MAX_PLAYERS]  # Up to 5 players' checkers

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates an empty board with the given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board to the console."""
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))  # Column labels (A, B, C, ...)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(board, col):
    """Checks if a column is valid for placing a checker."""
    return 0 <= col < len(board[0]) and board[0][col] == " "

def get_empty_row(board, col):
    """Returns the lowest empty row in the given column."""
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return None

def make_move(board, col, checker):
    """Places a checker in the specified column."""
    row = get_empty_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True
    return False

def check_winner(board, checker):
    """Checks if a given checker has won the game."""
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(cols):
        for row in range(rows - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (positive slope)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (negative slope)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw (no more valid moves)."""
    return all(board[0][col] != " " for col in range(len(board[0])))

def get_column_choice(board, current_player):
    """Prompts the current player to choose a column."""
    while True:
        try:
            choice = input(f"Player {current_player}, please enter a column: ").strip().upper()
            if len(choice) != 1 or not choice.isalpha():
                raise ValueError
            col = ord(choice) - 65  # Convert letter to column index
            if is_valid_column(board, col):
                return col
            else:
                print("Invalid move. Column is full or out of range. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid column letter.")

def main():
    """Main function to run the Connect 4 game."""
    # Initialize game
    board = create_board(ROWS, COLS)
    num_players = 2  # Fixed number of players for this submission
    players = CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    clear_screen()
    print_board(board)

    while True:
        # Get the current player's checker
        current_player = players[current_player_index]
        
        # Prompt for column choice
        col = get_column_choice(board, current_player)
        
        # Place the checker on the board
        make_move(board, col, current_player)
        
        # Clear screen and print board
        clear_screen()
        print_board(board)
        
        # Check for a winner
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for a draw
        if is_draw(board):
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
