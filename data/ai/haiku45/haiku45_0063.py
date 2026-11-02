import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the game board in a formatted manner.
    
    Args:
        board: The game board to print
    """
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+---" * cols + "+")


def get_column_input(num_players, current_player, cols):
    """
    Get and validate the column input from the player.
    
    Args:
        num_players: Total number of players
        current_player: Index of the current player (0-indexed)
        cols: Number of columns in the board
    
    Returns:
        The column index (0-indexed)
    """
    checker = CHECKERS[current_player]
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a column between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, current_player):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        col: Column index (0-indexed)
        current_player: Index of the current player
    
    Returns:
        True if the checker was placed successfully, False otherwise
    """
    checker = CHECKERS[current_player]
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False


def check_win(board, last_row, last_col, current_player):
    """
    Check if the current player has won the game.
    
    Args:
        board: The game board
        last_row: Row index of the last placed checker
        last_col: Column index of the last placed checker
        current_player: Index of the current player
    
    Returns:
        True if the current player has won, False otherwise
    """
    checker = CHECKERS[current_player]
    rows = len(board)
    cols = len(board[0])
    
    # Directions: right, down, down-right, down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        
        # Check in positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def check_draw(board):
    """
    Check if the game is a draw (board is full with no winner).
    
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


def get_first_player(num_players):
    """
    Randomly select the first player.
    
    Args:
        num_players: Total number of players
    
    Returns:
        Index of the first player (0-indexed)
    """
    return random.randint(0, num_players - 1)


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Select a random first player
    current_player = get_first_player(NUM_PLAYERS)
    
    # Print the initial board
    print_board(board)
    
    game_over = False
    winner = None
    
    # Game loop
    while not game_over:
        # Get valid column input from the player
        col = get_column_input(NUM_PLAYERS, current_player, COLS)
        
        # Try to place the checker
        if not place_checker(board, col, current_player):
            print("Column is full. Please choose another column.")
            continue
        
        # Print the updated board
        print_board(board)
        
        # Find the row where the checker was placed
        for row in range(ROWS):
            if board[row][col] == CHECKERS[current_player]:
                last_row = row
                break
        
        # Check for a win
        if check_win(board, last_row, col, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            game_over = True
            winner = current_player
        # Check for a draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to the next player
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
