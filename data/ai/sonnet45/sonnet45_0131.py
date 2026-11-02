import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def create_board():
    """Create and return an empty game board."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(NUM_COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board rows
    for row in range(NUM_ROWS):
        # Print top border
        print("  " + "+---" * NUM_COLS + "+")
        
        # Print row content
        print("  ", end="")
        for col in range(NUM_COLS):
            print(f"| {board[row][col]} ", end="")
        print("|")
    
    # Print bottom border
    print("  " + "+---" * NUM_COLS + "+")


def get_column_input(player_checker):
    """Get and validate column input from player."""
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
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board range
        if col_index < 0 or col_index >= NUM_COLS:
            print(f"Invalid column. Please choose between A and {chr(65 + NUM_COLS - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    Returns True if successful, False if column is full.
    """
    # Find the lowest available row in the column
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_win(board, checker):
    """Check if the specified player has won the game."""
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(NUM_ROWS - WIN_LENGTH + 1):
        for col in range(NUM_COLS):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - WIN_LENGTH + 1):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, NUM_ROWS):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """Check if the board is full (draw condition)."""
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Select players
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get column input
        col = get_column_input(current_checker)
        
        # Place checker
        if place_checker(board, col, current_checker):
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
        else:
            # Column is full, player loses turn
            print("Column is full! You lose your turn.")
            print_board(board)
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
