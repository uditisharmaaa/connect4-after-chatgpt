import os
import random

# Game configuration constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with all empty cells (whitespaces).
    
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
    Print the game board in the required format with column labels and grid lines.
    
    Args:
        board: The 2D list representing the game board
    """
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col) + "   ", end="")
    print()
    
    # Print each row with grid lines
    for row in range(rows):
        # Top border
        print("+---" * cols + "+")
        # Cell content
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Bottom border
    print("+---" * cols + "+")


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def get_valid_column(board, num_players, current_player_symbol):
    """
    Prompt the player for a column input and validate it.
    
    Args:
        board: The 2D list representing the game board
        num_players: Total number of players
        current_player_symbol: The symbol of the current player
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    cols = len(board[0])
    
    while True:
        player_num = PLAYER_SYMBOLS.index(current_player_symbol) + 1
        user_input = input(f"Player {current_player_symbol}, please enter a column: ").strip().upper()
        
        # Validate input length
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Validate column is within bounds
        if col < 0 or col >= cols:
            print(f"Invalid column. Please enter a column between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Validate column is not full
        if board[0][col] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, player_symbol):
    """
    Place a checker in the specified column at the lowest available row.
    
    Args:
        board: The 2D list representing the game board
        col: The column index (0-based) where to place the checker
        player_symbol: The symbol of the player
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest empty row in this column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_symbol
            return row
    
    return -1  # Column is full


def check_direction(board, row, col, player_symbol, drow, dcol):
    """
    Check if there are 4 checkers in a row in a specific direction.
    
    Args:
        board: The 2D list representing the game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        player_symbol: The symbol of the player
        drow: Row direction (-1, 0, or 1)
        dcol: Column direction (-1, 0, or 1)
    
    Returns:
        True if 4 checkers are found in this direction, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    count = 1  # Count the current checker
    
    # Check in the positive direction
    r, c = row + drow, col + dcol
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_symbol:
        count += 1
        r += drow
        c += dcol
    
    # Check in the negative direction
    r, c = row - drow, col - dcol
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_symbol:
        count += 1
        r -= drow
        c -= dcol
    
    return count >= WIN_LENGTH


def check_win(board, row, col, player_symbol):
    """
    Check if the current player has won after placing a checker.
    
    Args:
        board: The 2D list representing the game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        player_symbol: The symbol of the player
    
    Returns:
        True if the player has won, False otherwise
    """
    # Check horizontal
    if check_direction(board, row, col, player_symbol, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, player_symbol, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, player_symbol, 1, 1):
        return True
    
    # Check diagonal (top-right to bottom-left)
    if check_direction(board, row, col, player_symbol, 1, -1):
        return True
    
    return False


def check_draw(board):
    """
    Check if the board is completely filled (draw condition).
    
    Args:
        board: The 2D list representing the game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_next_player(current_player_index, num_players):
    """
    Get the next player's index.
    
    Args:
        current_player_index: Index of the current player
        num_players: Total number of players
    
    Returns:
        The index of the next player
    """
    return (current_player_index + 1) % num_players


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Create list of player symbols
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Display initial board
    clear_screen()
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player_symbol = players[current_player_index]
        
        # Get valid column from player
        col = get_valid_column(board, NUM_PLAYERS, current_player_symbol)
        
        # Place checker
        row = place_checker(board, col, current_player_symbol)
        
        # Clear screen and print updated board
        clear_screen()
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player_symbol):
            print(f"Player {current_player_symbol} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = get_next_player(current_player_index, NUM_PLAYERS)


def main():
    """Entry point of the program."""
    play_game()


if __name__ == "__main__":
    main()
