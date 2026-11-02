import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the game board to the console.
    
    Args:
        board: 2D list representing the game board
    """
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)} ", end=" ")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(cols):
        print("---+", end="")
    print()
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for _ in range(cols):
            print("---+", end="")
        print()


def is_valid_column(col_letter, cols):
    """
    Check if the column letter is valid.
    
    Args:
        col_letter: The column letter entered by the player
        cols: Number of columns in the board
    
    Returns:
        True if valid, False otherwise
    """
    if len(col_letter) != 1:
        return False
    if not col_letter.isalpha():
        return False
    col_letter = col_letter.upper()
    col_index = ord(col_letter) - ord('A')
    return 0 <= col_index < cols


def column_letter_to_index(col_letter):
    """
    Convert column letter to column index.
    
    Args:
        col_letter: The column letter (e.g., 'A', 'B', etc.)
    
    Returns:
        The column index (0-based)
    """
    return ord(col_letter.upper()) - ord('A')


def can_place_checker(board, col_index):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: 2D list representing the game board
        col_index: The column index
    
    Returns:
        True if a checker can be placed, False otherwise
    """
    return board[0][col_index] == ' '


def get_placement_row(board, col_index):
    """
    Get the row index where a checker should be placed in the given column.
    
    Args:
        board: 2D list representing the game board
        col_index: The column index
    
    Returns:
        The row index where the checker should be placed
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == ' ':
            return row
    return -1


def place_checker(board, col_index, checker):
    """
    Place a checker in the given column.
    
    Args:
        board: 2D list representing the game board
        col_index: The column index
        checker: The checker symbol to place
    
    Returns:
        True if successfully placed, False otherwise
    """
    row = get_placement_row(board, col_index)
    if row == -1:
        return False
    board[row][col_index] = checker
    return True


def check_horizontal_win(board, checker):
    """
    Check if there is a horizontal win for the given checker.
    
    Args:
        board: 2D list representing the game board
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
        board: 2D list representing the game board
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
        board: 2D list representing the game board
        checker: The checker symbol to check for
    
    Returns:
        True if there is a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonal from top-left to bottom-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal from top-right to bottom-left
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker):
    """
    Check if the given checker has won.
    
    Args:
        board: 2D list representing the game board
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
        board: 2D list representing the game board
    
    Returns:
        True if the board is full, False otherwise
    """
    return all(board[0][col] != ' ' for col in range(len(board[0])))


def get_player_move(board, num_players, current_player):
    """
    Get a valid move from the current player.
    
    Args:
        board: 2D list representing the game board
        num_players: Number of players in the game
        current_player: The current player index (0-based)
    
    Returns:
        The column index where the checker should be placed
    """
    cols = len(board[0])
    checker = CHECKERS[current_player]
    
    while True:
        col_letter = input(f"Player {checker}, please enter a column: ").upper()
        
        # Check if input is valid
        if not is_valid_column(col_letter, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = column_letter_to_index(col_letter)
        
        # Check if column is not full
        if not can_place_checker(board, col_index):
            print("This column is full. Please choose another column.")
            continue
        
        return col_index


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get player move
        col_index = get_player_move(board, NUM_PLAYERS, current_player)
        
        # Place checker
        checker = CHECKERS[current_player]
        place_checker(board, col_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
