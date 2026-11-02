import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_COUNT = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and initialize the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board rows
    for row in range(ROWS):
        # Print horizontal divider
        print("  ", end="")
        for col in range(COLS):
            print("+---", end="")
        print("+")
        
        # Print row content
        print("  ", end="")
        for col in range(COLS):
            print(f"| {board[row][col]} ", end="")
        print("|")
    
    # Print bottom border
    print("  ", end="")
    for col in range(COLS):
        print("+---", end="")
    print("+")

def get_valid_input(player_checker):
    """Get and validate user input for column selection."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - 65
        
        # Check if column is within bounds
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid input. Please enter a column between A and {chr(64 + COLS)}.")
            continue
        
        return col_index

def place_checker(board, col, checker):
    """Place a checker in the specified column. Returns True if successful, False if column is full."""
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the specified checker has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_COUNT + 1):
            if all(board[row][col + i] == checker for i in range(WIN_COUNT)):
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_COUNT + 1):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(WIN_COUNT)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_COUNT - 1, ROWS):
        for col in range(COLS - WIN_COUNT + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_COUNT)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_COUNT + 1):
        for col in range(COLS - WIN_COUNT + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_COUNT)):
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw condition)."""
    return all(board[0][col] != " " for col in range(COLS))

def play_game():
    """Main game loop."""
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    game_over = False
    
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get valid column input
        col = get_valid_input(current_checker)
        
        # Try to place the checker
        if not place_checker(board, col, current_checker):
            print("Column is full! You lose your turn.")
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
