import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board():
    """Create and return an empty board with all spaces."""
    board = []
    for row in range(ROWS):
        board.append([' ' for col in range(COLS)])
    return board


def print_board(board):
    """Print the board in the specified format."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+---" * COLS + "+")
    
    # Print each row
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+---" * COLS + "+")


def is_valid_column(column_letter):
    """Check if the column letter is valid."""
    if len(column_letter) != 1:
        return False
    if not column_letter.isalpha():
        return False
    column_index = ord(column_letter.upper()) - ord('A')
    if column_index < 0 or column_index >= COLS:
        return False
    return True


def get_column_index(column_letter):
    """Convert column letter to column index."""
    return ord(column_letter.upper()) - ord('A')


def can_place_checker(board, column_index):
    """Check if a checker can be placed in the column."""
    return board[0][column_index] == ' '


def place_checker(board, column_index, checker):
    """Place a checker in the column and return the row where it was placed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column_index] == ' ':
            board[row][column_index] = checker
            return row
    return -1


def check_win(board, row, col, checker):
    """Check if the last placed checker resulted in a win."""
    # Check horizontal
    count = 1
    # Check left
    j = col - 1
    while j >= 0 and board[row][j] == checker:
        count += 1
        j -= 1
    # Check right
    j = col + 1
    while j < COLS and board[row][j] == checker:
        count += 1
        j += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    i = row - 1
    while i >= 0 and board[i][col] == checker:
        count += 1
        i -= 1
    # Check down
    i = row + 1
    while i < ROWS and board[i][col] == checker:
        count += 1
        i += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0 and board[i][j] == checker:
        count += 1
        i -= 1
        j -= 1
    # Check down-right
    i, j = row + 1, col + 1
    while i < ROWS and j < COLS and board[i][j] == checker:
        count += 1
        i += 1
        j += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    i, j = row - 1, col + 1
    while i >= 0 and j < COLS and board[i][j] == checker:
        count += 1
        i -= 1
        j += 1
    # Check down-left
    i, j = row + 1, col - 1
    while i < ROWS and j >= 0 and board[i][j] == checker:
        count += 1
        i += 1
        j -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize the board
    board = initialize_board()
    
    # Get checkers for the players
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Main game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        current_checker = player_checkers[current_player_index]
        
        # Get valid input from the player
        valid_input = False
        while not valid_input:
            column_letter = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            
            # Check if input is valid
            if not is_valid_column(column_letter):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            column_index = get_column_index(column_letter)
            
            # Check if the column is not full
            if not can_place_checker(board, column_index):
                print("Column is full. Please choose another column.")
                continue
            
            valid_input = True
        
        # Place the checker
        row = place_checker(board, column_index, current_checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, row, column_index, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for a draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    play_game()
