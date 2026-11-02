import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols
SYMBOLS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, cols):
    """
    Initialize the game board with all empty spaces.
    
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
    Print the current state of the game board.
    
    Args:
        board: The current game board
    """
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
    
    print("+---" * cols + "+")


def is_valid_column(column_letter, cols):
    """
    Check if the input column letter is valid.
    
    Args:
        column_letter: The letter representing the column
        cols: Number of columns in the board
    
    Returns:
        True if valid, False otherwise
    """
    if len(column_letter) != 1:
        return False
    
    if not column_letter.isalpha():
        return False
    
    column_index = ord(column_letter.upper()) - ord('A')
    return 0 <= column_index < cols


def get_column_index(column_letter):
    """
    Convert column letter to column index.
    
    Args:
        column_letter: The letter representing the column
    
    Returns:
        The column index (0-based)
    """
    return ord(column_letter.upper()) - ord('A')


def can_place_checker(board, col):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The current game board
        col: The column index
    
    Returns:
        True if a checker can be placed, False otherwise
    """
    return board[0][col] == ' '


def place_checker(board, col, symbol):
    """
    Place a checker in the given column.
    
    Args:
        board: The current game board
        col: The column index
        symbol: The player's symbol
    
    Returns:
        The row where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    
    return -1


def check_win(board, row, col, symbol):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board: The current game board
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        symbol: The player's symbol
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal (top-left to bottom-right),
    # and diagonal (top-right to bottom-left)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
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
        board: The current game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for cell in board[0]:
        if cell == ' ':
            return False
    return True


def get_next_player(current_player, num_players):
    """
    Get the next player's turn.
    
    Args:
        current_player: The current player index (0-based)
        num_players: Total number of players
    
    Returns:
        The next player index
    """
    return (current_player + 1) % num_players


def get_player_input(num_players, current_player, cols):
    """
    Get and validate player input for column selection.
    
    Args:
        num_players: Total number of players
        current_player: The current player index
        cols: Number of columns in the board
    
    Returns:
        The valid column index
    """
    while True:
        player_symbol = SYMBOLS[current_player]
        column_letter = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        
        if not is_valid_column(column_letter, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        return get_column_index(column_letter)


def play_game(rows, cols, num_players):
    """
    Main game loop for Connect 4.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
        num_players: Number of players in the game
    """
    # Initialize the board
    board = initialize_board(rows, cols)
    
    # Randomly select the starting player
    current_player = random.randint(0, num_players - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        # Get player input
        col = get_player_input(num_players, current_player, cols)
        
        # Check if the column is full
        if not can_place_checker(board, col):
            print("Column is full. You lose your turn.")
            current_player = get_next_player(current_player, num_players)
            continue
        
        # Place the checker
        row = place_checker(board, col, SYMBOLS[current_player])
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, row, col, SYMBOLS[current_player]):
            print(f"Player {SYMBOLS[current_player]} won!")
            game_over = True
        # Check for a draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to the next player
            current_player = get_next_player(current_player, num_players)


def main():
    """
    Main entry point for the program.
    """
    play_game(ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
