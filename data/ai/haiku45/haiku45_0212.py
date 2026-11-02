import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Create and initialize a 2D board with all cells as whitespace.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the Connect 4 board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the Connect 4 board in the required format.
    
    Args:
        board: The 2D board to print
    """
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with separators
    for row in range(rows):
        # Print top separator
        print("+---" * cols + "+")
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom separator
    print("+---" * cols + "+")


def is_valid_input(user_input, cols):
    """
    Validate user input for column selection.
    
    Args:
        user_input: The user input string
        cols: Number of columns in the board
    
    Returns:
        True if valid, False otherwise
    """
    if len(user_input) != 1:
        return False
    
    if not user_input.isupper():
        return False
    
    col_index = ord(user_input) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False
    
    return True


def get_column_from_input(user_input):
    """
    Convert letter input to column index.
    
    Args:
        user_input: A single uppercase letter
    
    Returns:
        The column index (0-based)
    """
    return ord(user_input) - ord('A')


def is_column_full(board, col):
    """
    Check if a column is completely filled.
    
    Args:
        board: The game board
        col: Column index
    
    Returns:
        True if column is full, False otherwise
    """
    return board[0][col] != " "


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available position.
    
    Args:
        board: The game board
        col: Column index
        checker: The checker symbol to place
    
    Returns:
        The row index where checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest empty cell in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1


def check_horizontal_win(board, row, col, checker):
    """
    Check if there's a horizontal win at the given position.
    
    Args:
        board: The game board
        row: Row index of last placed checker
        col: Column index of last placed checker
        checker: The checker symbol to check
    
    Returns:
        True if win found, False otherwise
    """
    cols = len(board[0])
    count = 1
    
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    
    # Check right
    c = col + 1
    while c < cols and board[row][c] == checker:
        count += 1
        c += 1
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, checker):
    """
    Check if there's a vertical win at the given position.
    
    Args:
        board: The game board
        row: Row index of last placed checker
        col: Column index of last placed checker
        checker: The checker symbol to check
    
    Returns:
        True if win found, False otherwise
    """
    rows = len(board)
    count = 1
    
    # Check down
    r = row + 1
    while r < rows and board[r][col] == checker:
        count += 1
        r += 1
    
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    
    return count >= WIN_LENGTH


def check_diagonal_win(board, row, col, checker):
    """
    Check if there's a diagonal win at the given position.
    Checks both diagonals (/ and \).
    
    Args:
        board: The game board
        row: Row index of last placed checker
        col: Column index of last placed checker
        checker: The checker symbol to check
    
    Returns:
        True if win found, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
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
    while r < rows and c < cols and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < cols and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    
    # Check down-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board: The game board
        row: Row index of last placed checker
        col: Column index of last placed checker
        checker: The checker symbol to check
    
    Returns:
        True if win found, False otherwise
    """
    if check_horizontal_win(board, row, col, checker):
        return True
    
    if check_vertical_win(board, row, col, checker):
        return True
    
    if check_diagonal_win(board, row, col, checker):
        return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely filled.
    
    Args:
        board: The game board
    
    Returns:
        True if board is full, False otherwise
    """
    for cell in board[0]:
        if cell == " ":
            return False
    
    return True


def get_player_move(board, player_checker, cols):
    """
    Get a valid move from the current player.
    
    Args:
        board: The game board
        player_checker: The current player's checker symbol
        cols: Number of columns in the board
    
    Returns:
        The column index where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        
        if not is_valid_input(user_input, cols):
            print("Invalid input. Please enter a valid column letter (A-{}).".format(chr(65 + cols - 1)))
            continue
        
        col = get_column_from_input(user_input)
        
        if is_column_full(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Get list of player checkers
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        current_checker = players[current_player_index]
        
        # Get player's move
        col = get_player_move(board, current_checker, COLS)
        
        # Place checker on board
        row = place_checker(board, col, current_checker)
        
        # Print board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Main entry point for the Connect 4 game.
    """
    play_game()


if __name__ == "__main__":
    main()
