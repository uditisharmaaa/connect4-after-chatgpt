import os
import random

# Global constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, cols):
    """
    Initialize the board with empty spaces.
    
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
    Print the game board in the specified format.
    
    Args:
        board: The game board to print
    """
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(ord('A') + i)} ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * cols + "+")


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def is_valid_column(column_input, cols):
    """
    Validate the column input.
    
    Args:
        column_input: The user's input string
        cols: Number of columns in the board
    
    Returns:
        Column index (0-based) if valid, -1 otherwise
    """
    if len(column_input) != 1:
        return -1
    
    column_char = column_input.upper()
    
    if not column_char.isalpha():
        return -1
    
    col_index = ord(column_char) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index


def is_column_full(board, col):
    """
    Check if a column is full.
    
    Args:
        board: The game board
        col: Column index
    
    Returns:
        True if column is full, False otherwise
    """
    return board[0][col] != ' '


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        col: Column index
        checker: The checker symbol ('X', 'O', etc.)
    
    Returns:
        True if checker was placed successfully, False otherwise
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    
    return False


def check_horizontal_win(board, checker):
    """
    Check if there is a horizontal win.
    
    Args:
        board: The game board
        checker: The checker symbol to check for
    
    Returns:
        True if there is a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_vertical_win(board, checker):
    """
    Check if there is a vertical win.
    
    Args:
        board: The game board
        checker: The checker symbol to check for
    
    Returns:
        True if there is a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_diagonal_win(board, checker):
    """
    Check if there is a diagonal win (both directions).
    
    Args:
        board: The game board
        checker: The checker symbol to check for
    
    Returns:
        True if there is a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonal going down-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal going down-left
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker):
    """
    Check if the current player has won.
    
    Args:
        board: The game board
        checker: The checker symbol of the current player
    
    Returns:
        True if the player has won, False otherwise
    """
    return (check_horizontal_win(board, checker) or
            check_vertical_win(board, checker) or
            check_diagonal_win(board, checker))


def is_board_full(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: The game board
    
    Returns:
        True if board is full, False otherwise
    """
    for row in board:
        if ' ' in row:
            return False
    return True


def get_player_move(board, player_number, cols):
    """
    Get a valid move from the player.
    
    Args:
        board: The game board
        player_number: The player number (0-based)
        cols: Number of columns
    
    Returns:
        Column index (0-based) where the player places their checker
    """
    checker = PLAYER_CHECKERS[player_number]
    
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip()
        
        col = is_valid_column(user_input, cols)
        
        if col == -1:
            print("Invalid input. Please enter a valid column letter (A-{}).".format(
                chr(ord('A') + cols - 1)))
            continue
        
        if is_column_full(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col


def play_game():
    """Main game loop."""
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Clear screen and display initial board
    clear_screen()
    print("Welcome to Connect 4!")
    print()
    print_board(board)
    
    # Game loop
    while True:
        # Get player's move
        checker = PLAYER_CHECKERS[current_player]
        col = get_player_move(board, current_player, COLS)
        
        # Place the checker
        place_checker(board, col, checker)
        
        # Clear screen and display updated board
        clear_screen()
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
