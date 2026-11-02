import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
WINNING_LENGTH = 4
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(width, height):
    """
    Initialize the game board with empty spaces.
    
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
    Print the current state of the board to the console.
    
    Args:
        board: The game board to display
    """
    os.system('clear')
    width = len(board[0])
    height = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(width):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with borders
    for row in range(height):
        # Print top border of row
        print("+---" * width + "+")
        
        # Print row content
        print("|", end="")
        for col in range(width):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * width + "+")


def is_valid_input(column_letter, board):
    """
    Validate if the user input is a valid move.
    
    Args:
        column_letter: The column letter entered by the player
        board: The current game board
    
    Returns:
        True if the input is valid, False otherwise
    """
    # Check if input is a single uppercase letter
    if not isinstance(column_letter, str) or len(column_letter) != 1:
        return False
    
    if not column_letter.isupper():
        return False
    
    # Check if letter is within valid range
    column_index = ord(column_letter) - ord('A')
    if column_index < 0 or column_index >= len(board[0]):
        return False
    
    # Check if column is not full
    if board[0][column_index] != " ":
        return False
    
    return True


def place_checker(column_letter, player_checker, board):
    """
    Place a checker in the specified column.
    
    Args:
        column_letter: The column where the checker should be placed
        player_checker: The player's checker symbol
        board: The current game board
    
    Returns:
        True if placement was successful, False otherwise
    """
    column_index = ord(column_letter) - ord('A')
    
    # Find the lowest empty row in the column
    for row in range(len(board) - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = player_checker
            return True
    
    return False


def check_winner(board, player_checker):
    """
    Check if the current player has won the game.
    
    Args:
        board: The current game board
        player_checker: The player's checker symbol
    
    Returns:
        True if the player has won, False otherwise
    """
    height = len(board)
    width = len(board[0])
    
    # Check horizontal wins
    for row in range(height):
        for col in range(width - WINNING_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WINNING_LENGTH)):
                return True
    
    # Check vertical wins
    for col in range(width):
        for row in range(height - WINNING_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WINNING_LENGTH)):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(height - WINNING_LENGTH + 1):
        for col in range(width - WINNING_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WINNING_LENGTH)):
                return True
    
    # Check diagonal wins (top-right to bottom-left)
    for row in range(height - WINNING_LENGTH + 1):
        for col in range(WINNING_LENGTH - 1, width):
            if all(board[row + i][col - i] == player_checker for i in range(WINNING_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The current game board
    
    Returns:
        True if board is full, False otherwise
    """
    return all(board[0][col] != " " for col in range(len(board[0])))


def get_player_move(current_player_checker, board):
    """
    Get a valid move from the current player.
    
    Args:
        current_player_checker: The current player's checker symbol
        board: The current game board
    
    Returns:
        The column letter where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        
        if is_valid_input(user_input, board):
            return user_input
        else:
            print("Invalid input. Please enter a valid column letter.")


def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize the board
    board = initialize_board(BOARD_WIDTH, BOARD_HEIGHT)
    
    # Create list of player checkers
    player_checkers = CHECKERS[:PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, PLAYERS - 1)
    
    # Display the initial board
    print_board(board)
    
    # Main game loop
    while True:
        # Get current player's checker
        current_player_checker = player_checkers[current_player_index]
        
        # Get player's move
        column_letter = get_player_move(current_player_checker, board)
        
        # Place the checker
        place_checker(column_letter, current_player_checker, board)
        
        # Display the updated board
        print_board(board)
        
        # Check if the current player has won
        if check_winner(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            break
        
        # Check if the board is full (draw)
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Move to the next player
        current_player_index = (current_player_index + 1) % PLAYERS


def main():
    """
    Entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
