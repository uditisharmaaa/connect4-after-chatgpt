import os
import random

# Constants for board dimensions and game settings
ROWS = 6
COLS = 7
WIN_LENGTH = 4
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    """
    Create an empty game board with specified dimensions.
    
    Args:
        rows (int): Number of rows in the board
        cols (int): Number of columns in the board
    
    Returns:
        list: A 2D list representing the game board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the current state of the board to the screen.
    
    Args:
        board (list): The 2D game board
    """
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)}  ", end="")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
        print("+---" * cols + "+")


def is_valid_column(column, cols):
    """
    Check if the column input is valid.
    
    Args:
        column (str): The column letter input by the player
        cols (int): Number of columns in the board
    
    Returns:
        bool: True if the column is valid, False otherwise
    """
    if len(column) != 1:
        return False
    
    if not column.isalpha():
        return False
    
    col_index = ord(column.upper()) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False
    
    return True


def get_column_index(column):
    """
    Convert a column letter to its corresponding index.
    
    Args:
        column (str): The column letter
    
    Returns:
        int: The column index (0-based)
    """
    return ord(column.upper()) - ord('A')


def is_column_full(board, col_index):
    """
    Check if a column is completely filled.
    
    Args:
        board (list): The 2D game board
        col_index (int): The column index to check
    
    Returns:
        bool: True if the column is full, False otherwise
    """
    return board[0][col_index] != " "


def place_checker(board, col_index, symbol):
    """
    Place a checker in the specified column.
    
    Args:
        board (list): The 2D game board
        col_index (int): The column index where the checker will be placed
        symbol (str): The player's symbol
    
    Returns:
        bool: True if the checker was placed successfully, False otherwise
    """
    if is_column_full(board, col_index):
        return False
    
    # Find the lowest empty row in the column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return True
    
    return False


def check_direction(board, row, col, symbol, drow, dcol):
    """
    Check if there are 4 checkers in a row in a specific direction.
    
    Args:
        board (list): The 2D game board
        row (int): The row of the checker to start from
        col (int): The column of the checker to start from
        symbol (str): The player's symbol
        drow (int): Row direction (-1, 0, or 1)
        dcol (int): Column direction (-1, 0, or 1)
    
    Returns:
        int: The count of consecutive checkers in the specified direction
    """
    count = 0
    r, c = row, col
    
    while 0 <= r < len(board) and 0 <= c < len(board[0]):
        if board[r][c] == symbol:
            count += 1
        else:
            break
        r += drow
        c += dcol
    
    return count


def check_win(board, row, col, symbol):
    """
    Check if the last move resulted in a win for the player.
    
    Args:
        board (list): The 2D game board
        row (int): The row where the last checker was placed
        col (int): The column where the last checker was placed
        symbol (str): The player's symbol
    
    Returns:
        bool: True if the player won, False otherwise
    """
    # Directions to check: horizontal, vertical, and both diagonals
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for drow, dcol in directions:
        # Count in the positive direction
        count_positive = check_direction(board, row, col, symbol, drow, dcol)
        
        # Count in the negative direction
        count_negative = check_direction(board, row, col, symbol, -drow, -dcol)
        
        # Total count includes both directions minus 1 (to avoid counting the checker twice)
        total_count = count_positive + count_negative - 1
        
        if total_count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely filled.
    
    Args:
        board (list): The 2D game board
    
    Returns:
        bool: True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_player_input(current_player, cols):
    """
    Get and validate the column input from the current player.
    
    Args:
        current_player (str): The symbol of the current player
        cols (int): Number of columns in the board
    
    Returns:
        int: The valid column index
    """
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ")
        
        if is_valid_column(user_input, cols):
            return get_column_index(user_input)
        else:
            print("Invalid input. Please enter a valid column letter.")


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Create the board
    board = create_board(ROWS, COLS)
    
    # Determine the number of players and their symbols
    num_players = MIN_PLAYERS
    player_symbols = PLAYER_SYMBOLS[:num_players]
    
    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    
    # Print the initial board
    print_board(board)
    
    # Main game loop
    game_over = False
    
    while not game_over:
        current_symbol = player_symbols[current_player_index]
        
        # Get valid column input from the player
        col_index = get_player_input(current_symbol, COLS)
        
        # Try to place the checker
        if not place_checker(board, col_index, current_symbol):
            print("Column is full. Please choose another column.")
            print_board(board)
            continue
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        # Find the row where the checker was placed
        for row in range(ROWS):
            if board[row][col_index] == current_symbol:
                last_row = row
                break
        
        if check_win(board, last_row, col_index, current_symbol):
            print(f"Player {current_symbol} won!")
            game_over = True
        # Check for a draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        # Switch to the next player
        if not game_over:
            current_player_index = (current_player_index + 1) % num_players


def main():
    """
    Entry point for the Connect 4 game.
    """
    play_game()


if __name__ == "__main__":
    main()
