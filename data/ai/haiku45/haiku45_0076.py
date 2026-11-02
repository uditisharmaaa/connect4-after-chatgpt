import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the board with all empty spaces.
    
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
    Print the board in the specified format.
    
    Args:
        board: The 2D list representing the board
    """
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(65 + i)} ", end=" ")
    print()
    
    # Print board with separators
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * cols + "+")


def is_valid_column(column_input, cols):
    """
    Validate if the input is a valid column.
    
    Args:
        column_input: The user input for column selection
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based) if valid, -1 otherwise
    """
    if len(column_input) != 1:
        return -1
    
    if not column_input.isalpha():
        return -1
    
    column_index = ord(column_input.upper()) - ord('A')
    
    if column_index < 0 or column_index >= cols:
        return -1
    
    return column_index


def can_place_checker(board, col):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The 2D list representing the board
        col: The column index (0-based)
    
    Returns:
        True if a checker can be placed, False otherwise
    """
    return board[0][col] == " "


def place_checker(board, col, checker):
    """
    Place a checker in the given column.
    
    Args:
        board: The 2D list representing the board
        col: The column index (0-based)
        checker: The checker symbol to place
    
    Returns:
        True if placement was successful, False otherwise
    """
    # Find the lowest empty row in the column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_horizontal_win(board, checker):
    """
    Check if there is a horizontal win for the given checker.
    
    Args:
        board: The 2D list representing the board
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
    Check if there is a vertical win for the given checker.
    
    Args:
        board: The 2D list representing the board
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
    Check if there is a diagonal win for the given checker.
    
    Args:
        board: The 2D list representing the board
        checker: The checker symbol to check for
    
    Returns:
        True if there is a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonal down-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal down-left
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker):
    """
    Check if the given checker has won the game.
    
    Args:
        board: The 2D list representing the board
        checker: The checker symbol to check for
    
    Returns:
        True if there is a win, False otherwise
    """
    return (check_horizontal_win(board, checker) or 
            check_vertical_win(board, checker) or 
            check_diagonal_win(board, checker))


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The 2D list representing the board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    
    return True


def get_player_input(current_player, cols):
    """
    Get valid input from the current player.
    
    Args:
        current_player: The player number (0-based)
        cols: Number of columns in the board
    
    Returns:
        The valid column index (0-based)
    """
    checker = CHECKERS[current_player]
    
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip()
        
        column_index = is_valid_column(user_input, cols)
        
        if column_index == -1:
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue
        
        return column_index


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    while True:
        checker = CHECKERS[current_player]
        
        # Get valid column input from current player
        while True:
            column = get_player_input(current_player, COLUMNS)
            
            # Check if column is not full
            if can_place_checker(board, column):
                place_checker(board, column, checker)
                break
            else:
                print("Column is full. Please choose another column.")
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for a draw
        if is_board_full(board):
            print("Draw! The board is full.")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """
    Main entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
