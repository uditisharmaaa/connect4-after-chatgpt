import os
import random

# Constants (board dimensions and players)
ROWS = 6           # number of rows
COLUMNS = 7        # number of columns (max 26)
PLAYERS = 2        # number of players (2 to 5)
WIN_CONDITION = 4  # number of consecutive checkers to win

# Checkers assigned to players in order (X, O, V, H, M)
CHECKERS = ["X", "O", "V", "H", "M"]

# Validate the constants
assert 2 <= PLAYERS <= 5, "Number of players must be between 2 and 5."
assert 1 <= ROWS and 1 <= COLUMNS <= 26, "Rows and Columns must be positive, columns max 26."


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def create_board(rows, cols):
    """
    Create an empty board with 'rows' rows and 'cols' columns.
    Each cell initialized with a whitespace " ".
    
    Returns:
        board (list of list): 2D list representing the board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board with column labels and grid lines.
    
    Args:
        board (list of list): 2D list representing the board.
    """
    cols = len(board[0])
    # Print column labels (A-G)
    labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(labels))
    
    # Print the board rows
    for row in range(len(board)):
        print("+" + "---+" * cols)
        row_str = "|"
        for col in range(cols):
            row_str += f" {board[row][col]} |"
        print(row_str)
    print("+" + "---+" * cols)


def is_valid_column(input_str, cols):
    """
    Check if the input string is a valid column letter.
    
    Args:
        input_str (str): User input string.
        cols (int): Number of columns on the board.
        
    Returns:
        bool: True if input is a valid column label (A-G), False otherwise.
    """
    if len(input_str) != 1:
        return False
    letter = input_str.upper()
    if 'A' <= letter < chr(ord('A') + cols):
        return True
    return False


def is_column_full(board, col_index):
    """
    Check if a given column is full (no empty spaces).
    
    Args:
        board (list of list): The game board.
        col_index (int): Column index to check.
        
    Returns:
        bool: True if full, False if there is empty space.
    """
    # The top row (row 0) is the first to fill when column is full
    return board[0][col_index] != " "


def drop_checker(board, col_index, checker):
    """
    Drop a checker in the specified column.
    The checker falls to the lowest available empty row in that column.
    
    Args:
        board (list of list): The game board.
        col_index (int): Column index where checker will be placed.
        checker (str): The player's checker symbol.
        
    Returns:
        bool: True if placement successful, False if column is full.
    """
    rows = len(board)
    
    # Start from bottom row, move upward to find empty spot
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    # Column full, cannot place
    return False


def check_win(board, checker):
    """
    Check entire board if the given checker has 4 in a row:
    horizontally, vertically, or diagonally.
    
    Args:
        board (list of list): The game board.
        checker (str): The player's checker symbol.
        
    Returns:
        bool: True if checker has 4 in a row, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True
    
    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True
    
    return False


def check_draw(board):
    """
    Check if the board is full (no empty spaces).
    
    Args:
        board (list of list): The game board.
        
    Returns:
        bool: True if the board is full (draw), False otherwise.
    """
    for row in board:
        if " " in row:
            return False
    return True


def get_player_input(board, checker):
    """
    Prompt the player to input a column letter until a valid input is given.
    Valid input is a single uppercase letter corresponding to a non-full column.
    
    Args:
        board (list of list): The game board.
        checker (str): Player's checker symbol (for prompt).
        
    Returns:
        int: the column index (0-based) where checker can be placed,
             or None if column is full and player loses turn.
    """
    cols = len(board[0])
    
    while True:
        choice = input(f"Player {checker}, please enter a column: ").strip().upper()
        if not is_valid_column(choice, cols):
            # Invalid input (not a single letter A-G)
            continue
        
        col_index = ord(choice) - ord('A')
        
        # Check if column is full
        if is_column_full(board, col_index):
            # Turn is lost immediately
            return None
        
        return col_index


def main():
    # Initialize board and select random starting player
    board = create_board(ROWS, COLUMNS)
    players_order = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    
    while True:
        clear_screen()
        print_board(board)
        
        current_checker = players_order[current_player_index]
        col_index = get_player_input(board, current_checker)
        
        # If col_index is None, column full and turn lost
        if col_index is None:
            # Next player's turn
            current_player_index = (current_player_index + 1) % PLAYERS
            continue
        
        drop_checker(board, col_index, current_checker)
        
        # Check if current player won
        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break
        
        # Check if draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS


if __name__ == "__main__":
    main()
