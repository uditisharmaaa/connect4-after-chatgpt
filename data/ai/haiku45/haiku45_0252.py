import os
import random

# Global constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the game board with empty spaces.
    
    Returns:
        list: A 2D list representing the game board.
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the current game board with column labels and formatting.
    
    Args:
        board (list): The current game board.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(ord('A') + col)} ", end=" ")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(COLS):
        print("---+", end="")
    print()
    
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for _ in range(COLS):
            print("---+", end="")
        print()


def is_valid_column(col_input):
    """
    Validate if the column input is valid.
    
    Args:
        col_input (str): The column input from the user.
    
    Returns:
        int or None: The column index if valid, None otherwise.
    """
    if len(col_input) != 1:
        return None
    
    if not col_input.isalpha():
        return None
    
    col_index = ord(col_input.upper()) - ord('A')
    
    if col_index < 0 or col_index >= COLS:
        return None
    
    return col_index


def is_column_full(board, col):
    """
    Check if a column is full.
    
    Args:
        board (list): The current game board.
        col (int): The column index.
    
    Returns:
        bool: True if the column is full, False otherwise.
    """
    return board[0][col] != " "


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board (list): The current game board.
        col (int): The column index.
        checker (str): The checker symbol.
    
    Returns:
        bool: True if the checker was placed successfully, False otherwise.
    """
    if is_column_full(board, col):
        return False
    
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_winner(board, col, row, checker):
    """
    Check if the last move resulted in a win.
    
    Args:
        board (list): The current game board.
        col (int): The column index of the last move.
        row (int): The row index of the last move.
        checker (str): The checker symbol.
    
    Returns:
        bool: True if the player won, False otherwise.
    """
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < COLS and board[row][c] == checker:
        count += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    # Check down
    r = row + 1
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check top-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    # Check bottom-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check top-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check bottom-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def get_checker_row(board, col):
    """
    Get the row index where the checker was placed in the column.
    
    Args:
        board (list): The current game board.
        col (int): The column index.
    
    Returns:
        int: The row index where the checker was placed.
    """
    for row in range(ROWS):
        if board[row][col] != " ":
            return row
    return -1


def is_board_full(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board (list): The current game board.
    
    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_player_move(board, player_checker):
    """
    Get a valid move from the player.
    
    Args:
        board (list): The current game board.
        player_checker (str): The checker symbol of the current player.
    
    Returns:
        int: The column index where the checker should be placed.
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        col = is_valid_column(user_input)
        
        if col is None:
            print("Invalid input. Please enter a valid column letter (A-{}).".format(
                chr(ord('A') + COLS - 1)))
            continue
        
        if is_column_full(board, col):
            print("This column is full. Please choose another column.")
            continue
        
        return col


def play_game():
    """
    Main game loop for Connect 4.
    """
    board = initialize_board()
    
    # Get list of checkers for the players
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    game_over = False
    
    while not game_over:
        # Get current player's checker
        current_checker = player_checkers[current_player_idx]
        
        # Get player's move
        col = get_player_move(board, current_checker)
        
        # Place checker on the board
        place_checker(board, col, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Get the row where the checker was placed
        row = get_checker_row(board, col)
        
        # Check for win
        if check_winner(board, col, row, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


def main():
    """
    Main function to start the game.
    """
    play_game()


if __name__ == "__main__":
    main()
