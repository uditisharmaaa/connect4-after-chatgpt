import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the board with empty spaces.
    
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
    Print the board in a formatted way.
    
    Args:
        board: The game board (2D list)
    """
    os.system('clear')
    
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * cols + "+")


def is_valid_column(col_input, cols):
    """
    Validate if the column input is valid.
    
    Args:
        col_input: The user input (column letter)
        cols: Number of columns in the board
    
    Returns:
        A tuple (is_valid, column_index) where column_index is -1 if invalid
    """
    if len(col_input) != 1:
        return False, -1
    
    if not col_input.isalpha():
        return False, -1
    
    col_index = ord(col_input.upper()) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False, -1
    
    return True, col_index


def is_column_full(board, col_index):
    """
    Check if a column is full.
    
    Args:
        board: The game board (2D list)
        col_index: The column index to check
    
    Returns:
        True if the column is full, False otherwise
    """
    return board[0][col_index] != " "


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board (2D list)
        col_index: The column index where the checker should be placed
        checker: The checker symbol ('X', 'O', 'V', 'H', or 'M')
    
    Returns:
        True if the checker was placed successfully, False otherwise
    """
    # Find the lowest available row in the column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def get_next_player(current_player, num_players):
    """
    Get the next player's turn.
    
    Args:
        current_player: The current player index (0-based)
        num_players: Total number of players
    
    Returns:
        The next player's index
    """
    return (current_player + 1) % num_players


def check_win(board, checker, win_length=4):
    """
    Check if the specified checker has won.
    
    Args:
        board: The game board (2D list)
        checker: The checker symbol to check for a win
        win_length: Number of checkers in a row needed to win
    
    Returns:
        True if the checker has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - win_length + 1):
            if all(board[row][col + i] == checker for i in range(win_length)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - win_length + 1):
            if all(board[row + i][col] == checker for i in range(win_length)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - win_length + 1):
        for col in range(cols - win_length + 1):
            if all(board[row + i][col + i] == checker for i in range(win_length)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - win_length + 1):
        for col in range(win_length - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(win_length)):
                return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The game board (2D list)
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game(rows, cols, num_players):
    """
    Main game loop.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
        num_players: Number of players
    """
    # Initialize the board
    board = initialize_board(rows, cols)
    
    # Select a random starting player
    current_player = random.randint(0, num_players - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        checker = CHECKERS[current_player]
        
        # Get valid input from the player
        while True:
            user_input = input(f"Player {checker}, please enter a column: ").strip()
            is_valid, col_index = is_valid_column(user_input, cols)
            
            if not is_valid:
                print("Invalid input. Please enter a valid column letter (A-{}).".format(chr(65 + cols - 1)))
                continue
            
            if is_column_full(board, col_index):
                print("Column is full. Please choose another column.")
                continue
            
            break
        
        # Place the checker
        place_checker(board, col_index, checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, checker, WIN_LENGTH):
            print(f"Player {checker} won!")
            game_over = True
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to the next player
            current_player = get_next_player(current_player, num_players)


def main():
    """
    Main entry point of the program.
    """
    play_game(ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
