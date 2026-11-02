import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the console screen."""
    os.system('clear')  # Use 'cls' for Windows

def create_board(rows, cols):
    """Create an empty board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Display the board with column labels."""
    # Print column labels
    print("  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0]))))
    # Print board rows
    for row in board:
        print("+---" * len(board[0]) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    """Check if the column is valid for placing a checker."""
    if column < 0 or column >= len(board[0]):
        return False
    return board[0][column] == " "

def get_next_empty_row(column, board):
    """Find the next empty row in the given column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            return row
    return -1  # Column is full

def check_for_winner(board, symbol):
    """Check if the given symbol has won the game."""
    # Check horizontal win
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical win
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the board is full and it's a draw."""
    return all(board[0][col] != " " for col in range(len(board[0])))

def play_game():
    """Main function to play the Connect 4 game."""
    # Initialize the board and players
    board = create_board(ROWS, COLS)
    num_players = 2  # Set to 2 players (can support up to 5)
    player_symbols = PLAYER_SYMBOLS[:num_players]
    random.shuffle(player_symbols)

    # Randomly select the first player
    current_player_idx = random.randint(0, num_players - 1)
    
    # Game loop
    while True:
        clear_screen()
        print_board(board)
        current_player = player_symbols[current_player_idx]
        print(f"Player {current_player}, it's your turn.")

        # Get player input
        while True:
            try:
                column_letter = input("Please enter a column (A-G): ").strip().upper()
                column = ord(column_letter) - ord('A')
                if is_valid_column(column, board):
                    break
                else:
                    print("Invalid column. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid column (A-G).")

        # Place the checker in the board
        row = get_next_empty_row(column, board)
        board[row][column] = current_player

        # Check for a win
        if check_for_winner(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % num_players

# Run the game
if __name__ == "__main__":
    play_game()
