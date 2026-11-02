import os
import random
import string

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create a 2D board with the given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print column labels
    print("  A B C D E F G")
    
    # Print rows
    for row in board:
        print("+---" * len(row))
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * len(row))

def get_player_checker(player_num):
    """Get the checker for the given player."""
    return CHECKERS[player_num - 1]

def get_column_index(column_label):
    """Get the column index from the given label."""
    return ord(column_label.upper()) - ord('A')

def is_valid_input(input_str, cols):
    """Check if the input is valid."""
    if len(input_str)!= 1:
        return False
    if not input_str.isalpha():
        return False
    if get_column_index(input_str) >= cols:
        return False
    return True

def is_column_full(board, col_index):
    """Check if the column is full."""
    return board[0][col_index]!= " "

def place_checker(board, col_index, checker):
    """Place the checker in the column."""
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return

def check_win(board, checker):
    """Check if the given player has won."""
    # Check horizontal wins
    for row in board:
        for col_index in range(len(row) - 3):
            if row[col_index] == checker and row[col_index + 1] == checker and row[col_index + 2] == checker and row[col_index + 3] == checker:
                return True
    
    # Check vertical wins
    for col_index in range(len(board[0])):
        for row_index in range(len(board) - 3):
            if board[row_index][col_index] == checker and board[row_index + 1][col_index] == checker and board[row_index + 2][col_index] == checker and board[row_index + 3][col_index] == checker:
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row_index in range(len(board) - 3):
        for col_index in range(len(board[0]) - 3):
            if board[row_index][col_index] == checker and board[row_index + 1][col_index + 1] == checker and board[row_index + 2][col_index + 2] == checker and board[row_index + 3][col_index + 3] == checker:
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row_index in range(3, len(board)):
        for col_index in range(len(board[0]) - 3):
            if board[row_index][col_index] == checker and board[row_index - 1][col_index + 1] == checker and board[row_index - 2][col_index + 2] == checker and board[row_index - 3][col_index + 3] == checker:
                return True
    
    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    # Create the board
    board = create_board(BOARD_ROWS, BOARD_COLS)
    
    # Randomly select the first player
    current_player = random.randint(1, NUM_PLAYERS)
    
    # Game loop
    while True:
        print_board(board)
        print(f"Player {get_player_checker(current_player)}, please enter a column:")
        
        # Get user input
        input_str = input().upper()
        
        # Validate input
        while not is_valid_input(input_str, BOARD_COLS):
            print("Invalid input. Please enter a column label (A-G):")
            input_str = input().upper()
        
        # Get column index
        col_index = get_column_index(input_str)
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
        # Place checker
        place_checker(board, col_index, get_player_checker(current_player))
        
        # Check for win
        if check_win(board, get_player_checker(current_player)):
            print_board(board)
            print(f"Player {get_player_checker(current_player)} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch player
        current_player = (current_player % NUM_PLAYERS) + 1

if __name__ == "__main__":
    main()
