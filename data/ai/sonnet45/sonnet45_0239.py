import random
import os

# Global constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """
    Creates and returns an empty board with NUM_ROWS rows and NUM_COLS columns.
    All cells are initialized with whitespace.
    """
    board = []
    for i in range(NUM_ROWS):
        row = []
        for j in range(NUM_COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """
    Prints the board with column labels (A, B, C, ...) and grid lines.
    """
    # Print column labels
    print("  ", end="")
    for i in range(NUM_COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print each row with grid lines
    for row in range(NUM_ROWS):
        # Print top border of cells
        print("+", end="")
        for col in range(NUM_COLS):
            print("---+", end="")
        print()
        
        # Print cell contents
        print("|", end="")
        for col in range(NUM_COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col in range(NUM_COLS):
        print("---+", end="")
    print()

def is_valid_input(user_input, board):
    """
    Validates the user input.
    Returns True if input is a valid column letter and column is not full.
    Returns False otherwise.
    """
    # Check if input is a single character
    if len(user_input) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not user_input.isupper() or not user_input.isalpha():
        return False
    
    # Convert letter to column index
    col_index = ord(user_input) - 65
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= NUM_COLS:
        return False
    
    # Check if column is not full (top row has space)
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, column, checker):
    """
    Places a checker in the specified column at the lowest available position.
    Returns True if placement was successful, False otherwise.
    """
    col_index = ord(column) - 65
    
    # Find the lowest available row in the column
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False

def check_win_horizontal(board, checker):
    """
    Checks if there are 4 consecutive checkers horizontally.
    """
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and 
                board[row][col + 1] == checker and 
                board[row][col + 2] == checker and 
                board[row][col + 3] == checker):
                return True
    return False

def check_win_vertical(board, checker):
    """
    Checks if there are 4 consecutive checkers vertically.
    """
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if (board[row][col] == checker and 
                board[row + 1][col] == checker and 
                board[row + 2][col] == checker and 
                board[row + 3][col] == checker):
                return True
    return False

def check_win_diagonal(board, checker):
    """
    Checks if there are 4 consecutive checkers diagonally.
    Checks both diagonal directions (/ and \).
    """
    # Check diagonal (bottom-left to top-right: /)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and 
                board[row + 1][col + 1] == checker and 
                board[row + 2][col + 2] == checker and 
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal (top-left to bottom-right: \)
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
    Checks if the current player has won by checking all win conditions.
    """
    return (check_win_horizontal(board, checker) or 
            check_win_vertical(board, checker) or 
            check_win_diagonal(board, checker))

def check_draw(board):
    """
    Checks if the board is full (draw condition).
    Returns True if all cells in the top row are filled.
    """
    for col in range(NUM_COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_input(player_checker, board):
    """
    Prompts the player for input and validates it.
    Continues to ask until valid input is received.
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        
        if is_valid_input(user_input, board):
            return user_input
        else:
            print("Invalid input. Please enter a valid column letter.")

def main():
    """
    Main game loop for Connect 4.
    """
    # Create the board
    board = create_board()
    
    # Randomly select the starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Clear screen and print initial board
    os.system('clear')
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        player_checker = CHECKERS[current_player]
        
        # Get player input
        column = get_player_input(player_checker, board)
        
        # Place the checker
        place_checker(board, column, player_checker)
        
        # Clear screen and print updated board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
