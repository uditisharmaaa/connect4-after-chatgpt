import os
import random

# Game constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board(rows, cols):
    """
    Initialize the game board with all empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """
    Print the game board in a formatted manner.
    
    Args:
        board: The game board (2D list)
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print top border
    print(" ", end="")
    for _ in range(cols):
        print("+---", end="")
    print("+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        
        # Print bottom border of row
        print(" ", end="")
        for _ in range(cols):
            print("+---", end="")
        print("+")


def is_valid_move(board, col, cols):
    """
    Check if a move is valid (column exists and is not full).
    
    Args:
        board: The game board (2D list)
        col: The column index (0-based)
        cols: Number of columns in the board
    
    Returns:
        True if the move is valid, False otherwise
    """
    if col < 0 or col >= cols:
        return False
    if board[0][col] != " ":
        return False
    return True


def place_checker(board, col, checker, rows):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board (2D list)
        col: The column index (0-based)
        checker: The player's checker symbol
        rows: Number of rows in the board
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1


def get_player_input(cols):
    """
    Get and validate player input for column selection.
    
    Args:
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input("Enter a column (A-{}): ".format(chr(65 + cols - 1))).strip().upper()
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter, not a number or special character.")
            continue
        
        col = ord(user_input) - ord('A')
        
        if col < 0 or col >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        return col


def check_winner(board, col, row, checker, rows, cols):
    """
    Check if the current move results in a win.
    
    Args:
        board: The game board (2D list)
        col: The column index where the checker was placed
        row: The row index where the checker was placed
        checker: The player's checker symbol
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the current move results in a win, False otherwise
    """
    # Check horizontal
    count = 1
    # Check left
    j = col - 1
    while j >= 0 and board[row][j] == checker:
        count += 1
        j -= 1
    # Check right
    j = col + 1
    while j < cols and board[row][j] == checker:
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
    while i < rows and board[i][col] == checker:
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
    while i < rows and j < cols and board[i][j] == checker:
        count += 1
        i += 1
        j += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    i, j = row - 1, col + 1
    while i >= 0 and j < cols and board[i][j] == checker:
        count += 1
        i -= 1
        j += 1
    # Check down-left
    i, j = row + 1, col - 1
    while i < rows and j >= 0 and board[i][j] == checker:
        count += 1
        i += 1
        j -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board, rows, cols):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The game board (2D list)
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def play_game(rows, cols, num_players):
    """
    Main game loop for Connect 4.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
        num_players: Number of players (2-5)
    """
    # Initialize board
    board = initialize_board(rows, cols)
    
    # Select random starting player
    current_player = random.randint(0, num_players - 1)
    
    # Print initial board
    print_board(board, cols)
    print(f"Player {CHECKERS[current_player]} will start!\n")
    input("Press Enter to begin the game...")
    
    # Game loop
    game_over = False
    while not game_over:
        print_board(board, cols)
        
        # Get player input
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        col = get_player_input(cols)
        
        # Validate and place checker
        if not is_valid_move(board, col, cols):
            print("Column is full or invalid. Please try again.\n")
            continue
        
        # Place checker and get the row where it was placed
        row = place_checker(board, col, CHECKERS[current_player], rows)
        
        # Check for win
        if check_winner(board, col, row, CHECKERS[current_player], rows, cols):
            print_board(board, cols)
            print(f"Player {CHECKERS[current_player]} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board, rows, cols):
            print_board(board, cols)
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % num_players
            print()


def main():
    """
    Main entry point for the Connect 4 game.
    """
    play_game(BOARD_ROWS, BOARD_COLUMNS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
