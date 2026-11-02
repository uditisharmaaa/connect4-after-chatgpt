import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(NUM_COLS):
        print(f"{chr(65 + i)}   ", end="")
    print()
    
    # Print rows with borders
    for row in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("| ", end="")
        for col in range(NUM_COLS):
            print(f"{board[row][col]} | ", end="")
        print()
    print("+---" * NUM_COLS + "+")


def is_valid_input(column_input, board):
    """Check if the input is valid."""
    # Check if input is a single character
    if len(column_input) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not column_input.isupper() or not column_input.isalpha():
        return False
    
    # Check if column is within board range
    col_index = ord(column_input) - 65
    if col_index < 0 or col_index >= NUM_COLS:
        return False
    
    return True


def is_column_full(board, col_index):
    """Check if a column is full."""
    return board[0][col_index] != " "


def place_checker(board, col_index, checker):
    """Place a checker in the specified column."""
    # Find the lowest available row in the column
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False


def check_win(board, checker):
    """Check if the specified checker has won."""
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


def is_board_full(board):
    """Check if the board is full (draw condition)."""
    return all(board[0][col] != " " for col in range(NUM_COLS))


def get_player_input(board, player_checker):
    """Get valid input from the player."""
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ")
        
        if not is_valid_input(column_input, board):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = ord(column_input) - 65
        
        if is_column_full(board, col_index):
            print("Column is full. You lose your turn.")
            return -1
        
        return col_index


def play_game():
    """Main game loop."""
    board = create_board()
    
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        checker = CHECKERS[current_player]
        
        # Get player input
        col_index = get_player_input(board, checker)
        
        # Place checker if valid column
        if col_index != -1:
            place_checker(board, col_index, checker)
            
            # Print updated board
            print_board(board)
            
            # Check for win
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            
            # Check for draw
            if is_board_full(board):
                print("Game is a draw!")
                break
        else:
            # Print board again after invalid move
            print_board(board)
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
