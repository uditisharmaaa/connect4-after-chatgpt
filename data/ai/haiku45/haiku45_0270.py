import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def initialize_board():
    """Create and initialize the game board with empty spaces."""
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
    
    # Print board with rows
    for row in range(ROWS):
        print("+---" * COLUMNS + "+")
        print("|", end="")
        for col in range(COLUMNS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    print("+---" * COLUMNS + "+")

def get_next_available_row(board, col):
    """Return the next available row in a column, or -1 if column is full."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def is_valid_input(user_input, board):
    """Validate user input and return column index or -1 if invalid."""
    # Check if input is a single character
    if len(user_input) != 1:
        return -1
    
    # Check if input is a letter
    if not user_input.isalpha():
        return -1
    
    # Convert to uppercase
    user_input = user_input.upper()
    
    # Check if letter is within board range
    col = ord(user_input) - ord('A')
    if col < 0 or col >= COLUMNS:
        return -1
    
    # Check if column is not full
    if get_next_available_row(board, col) == -1:
        return -1
    
    return col

def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    row = get_next_available_row(board, col)
    if row != -1:
        board[row][col] = checker
        return row
    return -1

def check_horizontal_win(board, row, col, checker):
    """Check if there is a horizontal win starting from the given position."""
    count = 0
    # Check left
    c = col
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < COLUMNS and board[row][c] == checker:
        count += 1
        c += 1
    
    return count >= WIN_LENGTH

def check_vertical_win(board, row, col, checker):
    """Check if there is a vertical win starting from the given position."""
    count = 0
    # Check down
    r = row
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    
    return count >= WIN_LENGTH

def check_diagonal_win_down_right(board, row, col, checker):
    """Check diagonal win going down-right and up-left."""
    count = 0
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLUMNS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    count += 1  # Add the current position
    
    return count >= WIN_LENGTH

def check_diagonal_win_down_left(board, row, col, checker):
    """Check diagonal win going down-left and up-right."""
    count = 0
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLUMNS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    count += 1  # Add the current position
    
    return count >= WIN_LENGTH

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    if check_horizontal_win(board, row, col, checker):
        return True
    if check_vertical_win(board, row, col, checker):
        return True
    if check_diagonal_win_down_right(board, row, col, checker):
        return True
    if check_diagonal_win_down_left(board, row, col, checker):
        return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    # Initialize the board
    board = initialize_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        checker = CHECKERS[current_player]
        
        # Get valid input from player
        while True:
            user_input = input(f"Player {checker}, please enter a column: ")
            col = is_valid_input(user_input, board)
            
            if col != -1:
                break
            else:
                print("Invalid input. Please enter a valid column letter.")
        
        # Place checker
        row = place_checker(board, col, checker)
        
        # Print board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS

def main():
    """Entry point for the program."""
    play_game()

if __name__ == "__main__":
    main()
