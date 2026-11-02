import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Global variables
board = []
current_player = 0
players = []


def initialize_board():
    """Create and initialize the game board with empty spaces."""
    global board
    board = []
    for row in range(ROWS):
        new_row = []
        for col in range(COLUMNS):
            new_row.append(" ")
        board.append(new_row)


def get_column_letter(col_index):
    """Convert column index to letter (0 -> A, 1 -> B, etc.)."""
    return chr(ord('A') + col_index)


def print_board():
    """Print the game board to the console."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLUMNS):
        print(f"{get_column_letter(col)}   ", end="")
    print()
    
    # Print top border
    print("+---" * COLUMNS + "+")
    
    # Print each row
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLUMNS):
            print(f" {board[row][col]} |", end="")
        print()
        print("+---" * COLUMNS + "+")


def get_valid_input():
    """Get and validate player input for column selection."""
    while True:
        user_input = input(f"Player {players[current_player]}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col_index < 0 or col_index >= COLUMNS:
            print(f"Invalid column. Please enter a letter between A and {get_column_letter(COLUMNS - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("That column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(col_index):
    """Place the current player's checker in the specified column."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = players[current_player]
            return


def check_win():
    """Check if the current player has won the game."""
    player_checker = players[current_player]
    
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw():
    """Check if the board is full (draw condition)."""
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True


def next_player():
    """Move to the next player's turn."""
    global current_player
    current_player = (current_player + 1) % NUM_PLAYERS


def setup_game():
    """Initialize the game and randomly select the first player."""
    global current_player, players
    
    initialize_board()
    
    # Set up players with their checkers
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)


def play_game():
    """Main game loop."""
    setup_game()
    print_board()
    
    while True:
        # Get valid input from current player
        col_index = get_valid_input()
        
        # Place checker in the column
        place_checker(col_index)
        
        # Print updated board
        print_board()
        
        # Check for win
        if check_win():
            print(f"Player {players[current_player]} won!")
            break
        
        # Check for draw
        if check_draw():
            print("It's a draw!")
            break
        
        # Move to next player
        next_player()


# Main program
if __name__ == "__main__":
    play_game()
