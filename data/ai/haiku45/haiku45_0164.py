import os
import random

# Constants
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
    Print the current state of the game board.
    
    Args:
        board: The game board to print
    """
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)} ", end="")
    print()
    
    # Print board with separators
    for row in range(rows):
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()
        
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def get_valid_column(board, player_checker):
    """
    Get a valid column input from the player.
    
    Args:
        board: The game board
        player_checker: The checker symbol of the current player
    
    Returns:
        The column index (0-based) where the checker should be placed
    """
    cols = len(board[0])
    
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input length
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Validate column is within bounds
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, player_checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        col: The column index (0-based)
        player_checker: The checker symbol to place
    
    Returns:
        The row index (0-based) where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return row
    
    return -1


def check_horizontal_win(board, row, col, player_checker):
    """
    Check if there's a horizontal win from the given position.
    
    Args:
        board: The game board
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        player_checker: The checker symbol to check for
    
    Returns:
        True if there's a win, False otherwise
    """
    cols = len(board[0])
    count = 1
    
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == player_checker:
        count += 1
        c -= 1
    
    # Check right
    c = col + 1
    while c < cols and board[row][c] == player_checker:
        count += 1
        c += 1
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, player_checker):
    """
    Check if there's a vertical win from the given position.
    
    Args:
        board: The game board
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        player_checker: The checker symbol to check for
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    count = 1
    
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == player_checker:
        count += 1
        r -= 1
    
    # Check down
    r = row + 1
    while r < rows and board[r][col] == player_checker:
        count += 1
        r += 1
    
    return count >= WIN_LENGTH


def check_diagonal_win(board, row, col, player_checker):
    """
    Check if there's a diagonal win from the given position (both diagonals).
    
    Args:
        board: The game board
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        player_checker: The checker symbol to check for
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == player_checker:
        count += 1
        r -= 1
        c -= 1
    
    # Check down-right
    r, c = row + 1, col + 1
    while r < rows and c < cols and board[r][c] == player_checker:
        count += 1
        r += 1
        c += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < cols and board[r][c] == player_checker:
        count += 1
        r -= 1
        c += 1
    
    # Check down-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == player_checker:
        count += 1
        r += 1
        c -= 1
    
    return count >= WIN_LENGTH


def check_win(board, row, col, player_checker):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board: The game board
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        player_checker: The checker symbol to check for
    
    Returns:
        True if there's a win, False otherwise
    """
    return (check_horizontal_win(board, row, col, player_checker) or
            check_vertical_win(board, row, col, player_checker) or
            check_diagonal_win(board, row, col, player_checker))


def check_draw(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: The game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Get player checkers
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Clear screen and display initial board
    clear_screen()
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_player_checker = player_checkers[current_player_index]
        
        # Get valid column from player
        col = get_valid_column(board, current_player_checker)
        
        # Place checker
        row = place_checker(board, col, current_player_checker)
        
        # Clear screen and print updated board
        clear_screen()
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        
        # Move to next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """Entry point of the program."""
    play_game()


if __name__ == "__main__":
    main()
