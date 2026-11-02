import os
import random

# Global constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(width, height):
    """
    Initialize a board with given dimensions.
    All cells are filled with whitespace.
    
    Args:
        width: Number of columns
        height: Number of rows
    
    Returns:
        A 2D list representing the board
    """
    board = [[" " for _ in range(width)] for _ in range(height)]
    return board


def print_board(board):
    """
    Print the board in a formatted manner.
    
    Args:
        board: The game board (2D list)
    """
    os.system('clear')
    width = len(board[0])
    height = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(width):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print top border
    print("+" + "+".join(["---"] * width) + "+")
    
    # Print each row
    for row in range(height):
        print("|", end="")
        for col in range(width):
            print(f" {board[row][col]} |", end="")
        print()
        print("+" + "+".join(["---"] * width) + "+")


def get_column_input(player_checker, width):
    """
    Get and validate column input from the player.
    
    Args:
        player_checker: The checker symbol of the current player
        width: Number of columns on the board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col_index < 0 or col_index >= width:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + width - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, player_checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available position.
    
    Args:
        board: The game board (2D list)
        col: The column index (0-based) where to place the checker
        player_checker: The checker symbol to place
    
    Returns:
        True if checker was placed successfully, False if column is full
    """
    height = len(board)
    
    # Find the lowest empty row in the column (start from bottom)
    for row in range(height - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False


def check_win(board, player_checker):
    """
    Check if the given player has won the game.
    A player wins by getting 4 checkers in a row horizontally, vertically, or diagonally.
    
    Args:
        board: The game board (2D list)
        player_checker: The checker symbol to check for a win
    
    Returns:
        True if the player has won, False otherwise
    """
    height = len(board)
    width = len(board[0])
    
    # Check horizontal
    for row in range(height):
        for col in range(width - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(width):
        for row in range(height - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(height - WIN_LENGTH + 1):
        for col in range(width - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(height - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, width):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Check if the board is full (game is a draw).
    
    Args:
        board: The game board (2D list)
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        if " " in row:
            return False
    return True


def main():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(BOARD_WIDTH, BOARD_HEIGHT)
    
    # Print initial board
    print_board(board)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    game_over = False
    
    while not game_over:
        # Get current player's checker
        current_player_checker = CHECKERS[current_player_index]
        
        # Get valid column input
        valid_placement = False
        while not valid_placement:
            col = get_column_input(current_player_checker, BOARD_WIDTH)
            valid_placement = place_checker(board, col, current_player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        
        # Switch to next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
