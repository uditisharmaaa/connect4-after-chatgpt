import os
import random

# Global constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the board with all empty spaces.
    
    Returns:
        A 2D list representing the board with dimensions ROWS x COLS,
        filled with empty spaces.
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the board in the required format with column labels and borders.
    
    Args:
        board: A 2D list representing the current game board.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        # Print top border
        print("+---" * COLS + "+")
        
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLS + "+")


def get_valid_column(player_checker):
    """
    Get a valid column input from the player.
    
    Args:
        player_checker: The checker symbol for the current player.
    
    Returns:
        The column index (0-based) where the player wants to place their checker.
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within board dimensions
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        return col


def is_column_full(board, col):
    """
    Check if a column is completely full.
    
    Args:
        board: The current game board.
        col: The column index to check.
    
    Returns:
        True if the column is full, False otherwise.
    """
    return board[0][col] != " "


def place_checker(board, col, checker):
    """
    Place a checker in the specified column at the lowest available position.
    
    Args:
        board: The current game board.
        col: The column index where the checker will be placed.
        checker: The checker symbol to place.
    
    Returns:
        True if the checker was placed successfully, False if the column is full.
    """
    if is_column_full(board, col):
        print("Column is full. Please choose another column.")
        return False
    
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_win(board, col, row, checker):
    """
    Check if the last placed checker at (row, col) creates a winning condition.
    
    Args:
        board: The current game board.
        col: The column index of the last placed checker.
        row: The row index of the last placed checker.
        checker: The checker symbol that was just placed.
    
    Returns:
        True if there is a win, False otherwise.
    """
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < COLS and board[row][c] == checker:
        count += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    # Check down
    r = row + 1
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The current game board.
    
    Returns:
        True if the board is full, False otherwise.
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def get_checker_for_player(player_num):
    """
    Get the checker symbol for a given player number.
    
    Args:
        player_num: The player number (0-based).
    
    Returns:
        The checker symbol for the player.
    """
    return PLAYER_CHECKERS[player_num % len(PLAYER_CHECKERS)]


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board()
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        player_checker = get_checker_for_player(current_player)
        
        # Get valid column from player
        while True:
            col = get_valid_column(player_checker)
            
            # Try to place the checker
            if place_checker(board, col, player_checker):
                # Find the row where the checker was placed
                for row in range(ROWS):
                    if board[row][col] == player_checker:
                        last_row = row
                        break
                break
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, col, last_row, player_checker):
            print(f"Player {player_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("Draw! The board is full.")
            game_over = True
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """
    Entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
