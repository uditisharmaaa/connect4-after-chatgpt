import random
import os

# Global constants for game configuration
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """
    Create and initialize the game board with empty spaces.
    Returns a 2D list representing the board.
    """
    board = []
    for row in range(NUM_ROWS):
        board.append([" "] * NUM_COLS)
    return board

def print_board(board):
    """
    Print the current state of the board with column labels.
    """
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(NUM_COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print each row with borders
    for row in range(NUM_ROWS):
        # Print top border of row
        print("+---" * NUM_COLS + "+")
        # Print cell contents
        print("|", end="")
        for col in range(NUM_COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * NUM_COLS + "+")

def is_valid_column(column_input):
    """
    Check if the input is a valid column letter.
    Returns the column index if valid, -1 otherwise.
    """
    # Check if input is a single character
    if len(column_input) != 1:
        return -1
    
    # Convert to uppercase and check if it's a letter
    column_input = column_input.upper()
    if not column_input.isalpha():
        return -1
    
    # Convert letter to column index
    col_index = ord(column_input) - 65
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= NUM_COLS:
        return -1
    
    return col_index

def is_column_full(board, col):
    """
    Check if a column is completely filled.
    Returns True if full, False otherwise.
    """
    return board[0][col] != " "

def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    Returns True if successful, False if column is full.
    """
    # Check if column is full
    if is_column_full(board, col):
        return False
    
    # Find the lowest available row in the column
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False

def check_horizontal_win(board, checker):
    """
    Check for a horizontal win (4 in a row).
    """
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and
                board[row][col + 1] == checker and
                board[row][col + 2] == checker and
                board[row][col + 3] == checker):
                return True
    return False

def check_vertical_win(board, checker):
    """
    Check for a vertical win (4 in a row).
    """
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if (board[row][col] == checker and
                board[row + 1][col] == checker and
                board[row + 2][col] == checker and
                board[row + 3][col] == checker):
                return True
    return False

def check_diagonal_win(board, checker):
    """
    Check for a diagonal win (4 in a row).
    Checks both directions: / and \
    """
    # Check diagonal (bottom-left to top-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and
                board[row + 1][col + 1] == checker and
                board[row + 2][col + 2] == checker and
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and
                board[row - 1][col + 1] == checker and
                board[row - 2][col + 2] == checker and
                board[row - 3][col + 3] == checker):
                return True
    
    return False

def check_win(board, checker):
    """
    Check if the current player has won.
    Returns True if player won, False otherwise.
    """
    return (check_horizontal_win(board, checker) or
            check_vertical_win(board, checker) or
            check_diagonal_win(board, checker))

def is_board_full(board):
    """
    Check if the board is completely filled (draw condition).
    """
    for col in range(NUM_COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """
    Main game loop.
    """
    # Initialize the game
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get player input
        valid_move = False
        while not valid_move:
            user_input = input(f"Player {current_checker}, please enter a column: ")
            
            # Validate input
            col_index = is_valid_column(user_input)
            if col_index == -1:
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            # Check if column is full
            if is_column_full(board, col_index):
                print("Column is full. Please choose another column.")
                # Player loses turn if column is full
                valid_move = True
                break
            
            # Place the checker
            if place_checker(board, col_index, current_checker):
                valid_move = True
            else:
                print("Could not place checker. Please try again.")
        
        # Print updated board
        print_board(board)
        
        # Check for win (only if a checker was placed)
        if not is_column_full(board, col_index) or board[0][col_index] == current_checker:
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                game_over = True
                continue
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            game_over = True
            continue
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
