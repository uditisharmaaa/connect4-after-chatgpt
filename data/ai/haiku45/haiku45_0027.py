import os
import random

# Constants for game configuration
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the game board with proper formatting.
    
    Args:
        board: The game board to print
    """
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)}  ", end="")
    print()
    
    # Print top border
    print("+" + "+".join(["---"] * cols) + "+")
    
    # Print each row
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
        print("+" + "+".join(["---"] * cols) + "+")


def is_valid_column(column, cols):
    """
    Check if the input is a valid column.
    
    Args:
        column: The column input (should be a single uppercase letter)
        cols: Number of columns in the board
    
    Returns:
        True if valid, False otherwise
    """
    if len(column) != 1:
        return False
    if not column.isupper():
        return False
    if not column.isalpha():
        return False
    col_index = ord(column) - ord('A')
    if col_index < 0 or col_index >= cols:
        return False
    return True


def column_to_index(column):
    """
    Convert a column letter to its index.
    
    Args:
        column: The column letter (e.g., 'A', 'B', etc.)
    
    Returns:
        The column index (0-based)
    """
    return ord(column) - ord('A')


def can_place_checker(board, col_index):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The game board
        col_index: The column index
    
    Returns:
        True if a checker can be placed, False if column is full
    """
    return board[0][col_index] == " "


def place_checker(board, col_index, checker):
    """
    Place a checker in the given column at the lowest available position.
    
    Args:
        board: The game board
        col_index: The column index
        checker: The player's checker symbol
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1


def check_win(board, row, col, checker):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board: The game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The player's checker symbol
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal /, diagonal \
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, -1),  # diagonal /
        (1, 1)    # diagonal \
    ]
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The game board
    
    Returns:
        True if board is full, False otherwise
    """
    for cell in board[0]:
        if cell == " ":
            return False
    return True


def get_player_input(board, player_checker):
    """
    Get valid input from the current player.
    
    Args:
        board: The game board
        player_checker: The current player's checker symbol
    
    Returns:
        The valid column index
    """
    cols = len(board[0])
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input format
        if not is_valid_column(user_input, cols):
            print("Invalid input. Please enter a single uppercase letter (A-" + 
                  chr(ord('A') + cols - 1) + ").")
            continue
        
        col_index = column_to_index(user_input)
        
        # Check if column is full
        if not can_place_checker(board, col_index):
            print("This column is full. Please choose another column.")
            continue
        
        return col_index


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Get player checkers
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    print(f"Player {players[current_player_index]} will go first!")
    input("Press Enter to start the game...")
    
    # Game loop
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get player input and place checker
        col_index = get_player_input(board, current_checker)
        row_index = place_checker(board, col_index, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Main entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
