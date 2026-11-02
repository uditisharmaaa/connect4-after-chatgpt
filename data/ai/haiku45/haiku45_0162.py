import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, cols):
    """
    Initialize a 2D board with all cells containing whitespace.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the Connect 4 board in a formatted manner.
    
    Args:
        board: The 2D game board to print
    """
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(chr(ord('A') + i), end="   ")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
        print("+---" * cols + "+")


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def get_valid_column(num_cols):
    """
    Get a valid column input from the player.
    
    Args:
        num_cols: Number of columns in the board
    
    Returns:
        An integer representing the column index (0-based)
    """
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Validate input length
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Validate that it's a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Validate column is within bounds
        if col_index < 0 or col_index >= num_cols:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The 2D game board
        col: The column index where the checker should be placed
        checker: The player's checker symbol
    
    Returns:
        True if the checker was successfully placed, False if the column is full
    """
    rows = len(board)
    
    # Find the lowest empty cell in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    
    # Column is full
    print("Column is full. Please choose another column.")
    return False


def check_win(board, checker):
    """
    Check if the given checker has won the game.
    
    Args:
        board: The 2D game board
        checker: The player's checker symbol to check for a win
    
    Returns:
        True if the checker has 4 in a row, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The 2D game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def get_next_player(current_player, num_players):
    """
    Get the next player in turn order.
    
    Args:
        current_player: The index of the current player
        num_players: Total number of players
    
    Returns:
        The index of the next player
    """
    return (current_player + 1) % num_players


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Create list of player checkers
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Clear screen and display initial board
    clear_screen()
    print(f"Connect 4 Game with {NUM_PLAYERS} player(s)")
    print(f"Board dimensions: {ROWS} rows x {COLS} columns")
    print()
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_checker = players[current_player]
        print(f"Player {current_checker}, please enter a column:")
        
        # Get valid column from player
        col = get_valid_column(COLS)
        
        # Try to place the checker
        if place_checker(board, col, current_checker):
            # Clear screen and display updated board
            clear_screen()
            print_board(board)
            
            # Check for win
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                game_over = True
            
            # Check for draw
            elif check_draw(board):
                print("It's a draw!")
                game_over = True
            
            # Move to next player
            else:
                current_player = get_next_player(current_player, NUM_PLAYERS)
        
        else:
            # Invalid move (column full), try again without changing player
            clear_screen()
            print_board(board)


if __name__ == "__main__":
    play_game()
