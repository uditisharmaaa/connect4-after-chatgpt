import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]
MAX_COLS = 26


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
    Print the current state of the board.
    
    Args:
        board: The 2D list representing the board
    """
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(ord('A') + i)} ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Print top border
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()


def is_valid_column(column_input, cols):
    """
    Validate if the column input is valid.
    
    Args:
        column_input: The input string from the user
        cols: Number of columns in the board
    
    Returns:
        Tuple (is_valid, column_index) where is_valid is True if valid
    """
    if len(column_input) != 1:
        return False, -1
    
    column_input = column_input.upper()
    
    if not column_input.isalpha():
        return False, -1
    
    col_index = ord(column_input) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False, -1
    
    return True, col_index


def is_column_full(board, col):
    """
    Check if a column is full.
    
    Args:
        board: The 2D list representing the board
        col: Column index
    
    Returns:
        True if column is full, False otherwise
    """
    return board[0][col] != " "


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The 2D list representing the board
        col: Column index
        checker: The checker symbol to place
    
    Returns:
        True if placement was successful, False if column is full
    """
    rows = len(board)
    
    if is_column_full(board, col):
        return False
    
    # Find the lowest empty row in this column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_win(board, row, col, checker):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board: The 2D list representing the board
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        checker: The checker symbol
    
    Returns:
        True if there is a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal-right, diagonal-left
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal right
        (1, -1)   # Diagonal left
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
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
        board: The 2D list representing the board
    
    Returns:
        True if board is full, False otherwise
    """
    for cell in board[0]:
        if cell == " ":
            return False
    return True


def get_last_row(board, col):
    """
    Get the row index where the last checker was placed in a column.
    
    Args:
        board: The 2D list representing the board
        col: Column index
    
    Returns:
        Row index of the last placed checker, or -1 if column is empty
    """
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][col] != " ":
            return row
    return -1


def play_turn(board, player_checker, cols):
    """
    Execute one player's turn.
    
    Args:
        board: The 2D list representing the board
        player_checker: The checker symbol for the current player
        cols: Number of columns in the board
    
    Returns:
        Tuple (success, row, col) where success is True if turn was completed
    """
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ")
        
        is_valid, col_index = is_valid_column(column_input, cols)
        
        if not is_valid:
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        if is_column_full(board, col_index):
            print("That column is full. Please choose another column.")
            continue
        
        # Place the checker
        if place_checker(board, col_index, player_checker):
            row = get_last_row(board, col_index)
            return True, row, col_index
        
        print("Error placing checker. Please try again.")


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Create list of checkers for the players
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    game_over = False
    
    while not game_over:
        current_checker = player_checkers[current_player_index]
        
        # Execute the current player's turn
        success, row, col = play_turn(board, current_checker, COLS)
        
        if success:
            # Print updated board
            print_board(board)
            
            # Check for win
            if check_win(board, row, col, current_checker):
                print(f"Player {current_checker} won!")
                game_over = True
            
            # Check for draw
            elif is_board_full(board):
                print("It's a draw!")
                game_over = True
            
            else:
                # Switch to next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print("Turn failed. Please try again.")


def main():
    """
    Entry point for the program.
    """
    play_game()


if __name__ == "__main__":
    main()
