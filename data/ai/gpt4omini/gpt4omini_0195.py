import os
import random

# Constants for game configuration
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = "XOVHM"  # Checkers for up to 5 players

def initialize_board():
    """Initialize the game board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board to the terminal."""
    os.system('clear')  # Clear the terminal
    header = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))  # Column labels A-G
    print(header)
    print("+---" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLUMNS)

def select_first_player(num_players):
    """Randomly select the first player from the available players."""
    return random.randint(0, num_players - 1)

def is_valid_input(column_input):
    """Check if the input is a valid column choice."""
    return len(column_input) == 1 and column_input.isalpha() and column_input.upper() in [chr(65 + i) for i in range(COLUMNS)]

def find_available_row(board, column):
    """Find the lowest available row in the selected column."""
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            return row
    return -1  # Column is full

def place_checker(board, column, checker):
    """Place the checker in the appropriate column."""
    row = find_available_row(board, column)
    if row != -1:
        board[row][column] = checker
        return True
    return False

def check_win(board, checker):
    """Check for a win condition for the given checker."""
    # Check horizontal, vertical, and diagonal connections
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    
    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    
    # Diagonal (\) check
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    
    # Diagonal (/) check
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(board[0][c] != " " for c in range(COLUMNS))

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    num_players = min(MAX_PLAYERS, len(PLAYER_CHECKERS))
    current_player = select_first_player(num_players)

    print_board(board)
    
    while True:
        checker = PLAYER_CHECKERS[current_player]
        column_input = input(f"Player {checker}, please enter a column: ").upper()
        
        while not is_valid_input(column_input):
            print("Invalid input. Please enter a letter from A to G.")
            column_input = input(f"Player {checker}, please enter a column: ").upper()
        
        column = ord(column_input) - 65  # Convert letter to column index
        
        if not place_checker(board, column, checker):
            print(f"Column {column_input} is full. Try again.")
            continue

        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    play_game()
