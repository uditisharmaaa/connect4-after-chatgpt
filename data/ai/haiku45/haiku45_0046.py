import os
import random

# Constants for board dimensions and players
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Initialize the board with empty spaces."""
    board = []
    for row in range(ROWS):
        board.append([" " for col in range(COLUMNS)])
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLUMNS):
        print(chr(65 + col), end="   ")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        # Print top border
        print("+", end="")
        for col in range(COLUMNS):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col in range(COLUMNS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col in range(COLUMNS):
        print("---+", end="")
    print()

def get_valid_input(current_player_checker):
    """Get valid column input from the player."""
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board range
        if col_index < 0 or col_index >= COLUMNS:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + COLUMNS - 1)}.")
            continue
        
        return col_index

def is_column_full(board, col_index):
    """Check if a column is completely filled."""
    return board[0][col_index] != " "

def place_checker(board, col_index, checker):
    """Place a checker in the specified column and return the row it was placed in."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    return -1  # Column is full

def check_horizontal_win(board, row, col, checker):
    """Check if there's a horizontal win at the given position."""
    count = 1
    
    # Check to the left
    col_check = col - 1
    while col_check >= 0 and board[row][col_check] == checker:
        count += 1
        col_check -= 1
    
    # Check to the right
    col_check = col + 1
    while col_check < COLUMNS and board[row][col_check] == checker:
        count += 1
        col_check += 1
    
    return count >= 4

def check_vertical_win(board, row, col, checker):
    """Check if there's a vertical win at the given position."""
    count = 1
    
    # Check downward
    row_check = row + 1
    while row_check < ROWS and board[row_check][col] == checker:
        count += 1
        row_check += 1
    
    # Check upward
    row_check = row - 1
    while row_check >= 0 and board[row_check][col] == checker:
        count += 1
        row_check -= 1
    
    return count >= 4

def check_diagonal_win(board, row, col, checker):
    """Check if there's a diagonal win at the given position."""
    # Check diagonal from top-left to bottom-right
    count = 1
    
    # Check up-left
    row_check = row - 1
    col_check = col - 1
    while row_check >= 0 and col_check >= 0 and board[row_check][col_check] == checker:
        count += 1
        row_check -= 1
        col_check -= 1
    
    # Check down-right
    row_check = row + 1
    col_check = col + 1
    while row_check < ROWS and col_check < COLUMNS and board[row_check][col_check] == checker:
        count += 1
        row_check += 1
        col_check += 1
    
    if count >= 4:
        return True
    
    # Check diagonal from top-right to bottom-left
    count = 1
    
    # Check up-right
    row_check = row - 1
    col_check = col + 1
    while row_check >= 0 and col_check < COLUMNS and board[row_check][col_check] == checker:
        count += 1
        row_check -= 1
        col_check += 1
    
    # Check down-left
    row_check = row + 1
    col_check = col - 1
    while row_check < ROWS and col_check >= 0 and board[row_check][col_check] == checker:
        count += 1
        row_check += 1
        col_check -= 1
    
    return count >= 4

def check_win(board, row, col, checker):
    """Check if the current move results in a win."""
    if check_horizontal_win(board, row, col, checker):
        return True
    if check_vertical_win(board, row, col, checker):
        return True
    if check_diagonal_win(board, row, col, checker):
        return True
    
    return False

def is_board_full(board):
    """Check if the board is completely filled."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    # Initialize the board
    board = initialize_board()
    
    # Randomly select the starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = CHECKERS[current_player_index]
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get valid input from the current player
        col_index = get_valid_input(current_player_checker)
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("Column is full. You lose your turn.")
        else:
            # Place the checker and get the row it was placed in
            row = place_checker(board, col_index, current_player_checker)
            
            # Print the updated board
            print_board(board)
            
            # Check for a win
            if check_win(board, row, col_index, current_player_checker):
                print(f"Player {current_player_checker} won!")
                break
            
            # Check for a draw
            if is_board_full(board):
                print("It's a draw!")
                break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_player_checker = CHECKERS[current_player_index]

# Run the game
if __name__ == "__main__":
    play_game()
