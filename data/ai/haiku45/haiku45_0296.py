import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, cols):
    """
    Print the current state of the board with proper formatting.
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)} ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()
    
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()


def get_column_input(cols, board):
    """
    Get valid column input from the player.
    Returns the column index (0-based).
    """
    while True:
        user_input = input("Player {}, please enter a column: ".format(current_player_checker)).upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, checker, rows, cols):
    """
    Place a checker in the specified column.
    Returns True if successful, False if column is full.
    """
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_win(board, rows, cols, checker, win_length=4):
    """
    Check if the specified checker has won.
    Returns True if the checker has 4 or more in a row.
    """
    # Check horizontal
    for row in range(rows):
        for col in range(cols - win_length + 1):
            if all(board[row][col + i] == checker for i in range(win_length)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - win_length + 1):
            if all(board[row + i][col] == checker for i in range(win_length)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - win_length + 1):
        for col in range(cols - win_length + 1):
            if all(board[row + i][col + i] == checker for i in range(win_length)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - win_length + 1):
        for col in range(win_length - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(win_length)):
                return True
    
    return False


def check_draw(board, rows, cols):
    """
    Check if the board is full (draw condition).
    Returns True if the board is full.
    """
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    global current_player_checker
    
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLS)
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_player_checker = CHECKERS[current_player]
        
        # Get player input
        col = get_column_input(COLS, board)
        
        # Place checker
        place_checker(board, col, current_player_checker, ROWS, COLS)
        
        # Print updated board
        print_board(board, COLS)
        
        # Check for win
        if check_win(board, ROWS, COLS, current_player_checker, WIN_LENGTH):
            print(f"Player {current_player_checker} won!")
            game_over = True
            break
        
        # Check for draw
        if check_draw(board, ROWS, COLS):
            print("It's a draw!")
            game_over = True
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    current_player_checker = ""
    play_game()
