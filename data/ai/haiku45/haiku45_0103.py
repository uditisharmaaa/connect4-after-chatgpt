import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board(rows, cols):
    """
    Initialize the board with empty cells (whitespace).
    
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
    Print the board in a formatted way with column labels and borders.
    
    Args:
        board: The game board to print
    """
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Top border
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()
        
        # Row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Bottom border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()


def is_valid_column(column_input, cols):
    """
    Validate if the column input is valid.
    
    Args:
        column_input: The user input for column
        cols: Number of columns in the board
    
    Returns:
        The column index if valid, -1 otherwise
    """
    if len(column_input) != 1:
        return -1
    
    if not column_input.isalpha():
        return -1
    
    column_input = column_input.upper()
    col_index = ord(column_input) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index


def can_place_checker(board, col_index):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The game board
        col_index: The column index
    
    Returns:
        True if a checker can be placed, False otherwise
    """
    return board[0][col_index] == " "


def place_checker(board, col_index, checker):
    """
    Place a checker in the given column.
    
    Args:
        board: The game board
        col_index: The column index
        checker: The checker symbol
    
    Returns:
        True if placement was successful, False otherwise
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def check_win(board, checker):
    """
    Check if the given checker has won the game.
    
    Args:
        board: The game board
        checker: The checker symbol to check for
    
    Returns:
        True if the checker has won, False otherwise
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


def is_board_full(board):
    """
    Check if the board is completely filled.
    
    Args:
        board: The game board
    
    Returns:
        True if the board is full, False otherwise
    """
    return all(board[0][col] != " " for col in range(len(board[0])))


def get_player_input(player_num, num_cols):
    """
    Get valid column input from the player.
    
    Args:
        player_num: The player number (0-indexed)
        num_cols: Number of columns in the board
    
    Returns:
        The valid column index
    """
    checker = CHECKERS[player_num]
    
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip()
        col_index = is_valid_column(user_input, num_cols)
        
        if col_index == -1:
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        if not can_place_checker(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def play_game(board, num_players):
    """
    Main game loop.
    
    Args:
        board: The game board
        num_players: Number of players in the game
    """
    rows = len(board)
    cols = len(board[0])
    
    # Randomly select the starting player
    current_player = random.randint(0, num_players - 1)
    
    print_board(board)
    
    # Game loop
    while True:
        # Get player input
        col_index = get_player_input(current_player, cols)
        
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
        
        # Move to next player
        current_player = (current_player + 1) % num_players


def main():
    """
    Main function to start the game.
    """
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    play_game(board, NUM_PLAYERS)


if __name__ == "__main__":
    main()
