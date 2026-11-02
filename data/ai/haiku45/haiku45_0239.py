import os
import random

# Constants
BOARD_COLS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize a 2D board with empty spaces.
    
    Args:
        rows: Number of rows
        cols: Number of columns
    
    Returns:
        A 2D list representing the board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the current state of the board with column labels and formatting.
    
    Args:
        board: 2D list representing the board
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
        col_letter: Column letter provided by user
        cols: Number of columns
    
    Returns:
        Column index if valid, -1 otherwise
    """
    if not col_letter or len(col_letter) != 1:
        return -1
    
    col_letter = col_letter.upper()
    
    if not col_letter.isalpha():
        return -1
    
    col_index = ord(col_letter) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index


def can_place_checker(board, col_index):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: 2D list representing the board
        col_index: Column index
    
    Returns:
        True if checker can be placed, False otherwise
    """
    if board[0][col_index] == " ":
        return True
    return False


def place_checker(board, col_index, player_checker):
    """
    Place a checker in the specified column and return the row where it was placed.
    
    Args:
        board: 2D list representing the board
        col_index: Column index
        player_checker: Checker symbol for the player
    
    Returns:
        Row index where checker was placed, -1 if unable to place
    """
    rows = len(board)
    
    # Find the lowest empty row in this column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            return row
    
    return -1


def check_win(board, row, col, player_checker):
    """
    Check if the player has won after placing a checker at (row, col).
    
    Args:
        board: 2D list representing the board
        row: Row index of last placed checker
        col: Column index of last placed checker
        player_checker: Checker symbol for the player
    
    Returns:
        True if player won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == player_checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < cols and board[row][c] == player_checker:
        count += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check down
    r = row + 1
    while r < rows and board[r][col] == player_checker:
        count += 1
        r += 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == player_checker:
        count += 1
        r -= 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == player_checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < rows and c < cols and board[r][c] == player_checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < cols and board[r][c] == player_checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == player_checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: 2D list representing the board
    
    Returns:
        True if board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize board
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    
    # Get player checkers
    player_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Choose random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    while True:
        current_checker = player_checkers[current_player]
        
        # Get valid input from player
        while True:
            player_input = input(f"Player {current_checker}, please enter a column: ")
            
            col_index = is_valid_column(player_input, BOARD_COLS)
            
            if col_index == -1:
                print("Invalid column. Please enter a valid column letter (A-" + 
                      chr(ord('A') + BOARD_COLS - 1) + ").")
                continue
            
            if not can_place_checker(board, col_index):
                print("Column is full. Please choose another column.")
                continue
            
            break
        
        # Place the checker
        row = place_checker(board, col_index, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col_index, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
