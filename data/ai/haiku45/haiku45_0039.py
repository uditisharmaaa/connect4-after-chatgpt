import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    """
    Create and initialize a 2D board with all cells containing spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
        
    Returns:
        A 2D list representing the game board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """
    Print the game board in a formatted grid.
    
    Args:
        board: The 2D list representing the game board
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(chr(ord('A') + i), end="   ")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * cols + "+")


def is_valid_move(board, col, cols):
    """
    Check if a move to the specified column is valid.
    
    Args:
        board: The 2D list representing the game board
        col: Column index (0-indexed)
        cols: Number of columns in the board
        
    Returns:
        True if the move is valid, False otherwise
    """
    if col < 0 or col >= cols:
        return False
    if board[0][col] != " ":
        return False
    return True


def get_next_open_row(board, col, rows):
    """
    Get the next open row in a column where a checker can be placed.
    
    Args:
        board: The 2D list representing the game board
        col: Column index (0-indexed)
        rows: Number of rows in the board
        
    Returns:
        The row index where the checker should be placed, or -1 if column is full
    """
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


def place_checker(board, row, col, player_checker):
    """
    Place a checker on the board at the specified position.
    
    Args:
        board: The 2D list representing the game board
        row: Row index where checker is placed
        col: Column index where checker is placed
        player_checker: The checker symbol for the player
    """
    board[row][col] = player_checker


def get_player_move(board, cols, current_player, player_checker):
    """
    Get a valid move from the current player.
    
    Args:
        board: The 2D list representing the game board
        cols: Number of columns in the board
        current_player: Current player number (1-indexed)
        player_checker: The checker symbol for the player
        
    Returns:
        The column index (0-indexed) where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input length
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Validate column is in range
        if col < 0 or col >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Validate move is valid
        if not is_valid_move(board, col, cols):
            print("Invalid move. Column is full or does not exist.")
            continue
        
        return col


def check_win(board, row, col, player_checker, rows, cols):
    """
    Check if the current player has won the game.
    
    Args:
        board: The 2D list representing the game board
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        player_checker: The checker symbol for the player
        rows: Number of rows in the board
        cols: Number of columns in the board
        
    Returns:
        True if the player has won, False otherwise
    """
    # Check horizontal
    count = 0
    for c in range(cols):
        if board[row][c] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(rows):
        if board[r][col] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    # Find starting position
    start_row = row
    start_col = col
    while start_row < rows - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    
    r, c = start_row, start_col
    while r >= 0 and c < cols:
        if board[r][c] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    # Find starting position
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    
    r, c = start_row, start_col
    while r < rows and c < cols:
        if board[r][c] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    return False


def is_board_full(board, rows, cols):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The 2D list representing the game board
        rows: Number of rows in the board
        cols: Number of columns in the board
        
    Returns:
        True if the board is full, False otherwise
    """
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize board
    board = create_board(ROWS, COLS)
    
    # Print initial board
    print_board(board, COLS)
    
    # Randomly select starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    while True:
        # Get current player's checker
        player_checker = PLAYER_CHECKERS[current_player]
        
        # Get player's move
        col = get_player_move(board, COLS, current_player + 1, player_checker)
        
        # Find the row where the checker will be placed
        row = get_next_open_row(board, col, ROWS)
        
        # Place the checker
        place_checker(board, row, col, player_checker)
        
        # Print the board
        print_board(board, COLS)
        
        # Check for win
        if check_win(board, row, col, player_checker, ROWS, COLS):
            print(f"Player {player_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board, ROWS, COLS):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """
    Main entry point for the Connect 4 game.
    """
    play_game()


if __name__ == "__main__":
    main()
