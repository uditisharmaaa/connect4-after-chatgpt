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
        A 2D list representing the board
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the current state of the board.
    
    Args:
        board: The current game board
    """
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)} ", end=" ")
    print()
    
    # Print board with separators
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


def get_valid_input(board, num_players):
    """
    Get and validate player input for column selection.
    
    Args:
        board: The current game board
        num_players: Number of players in the game
    
    Returns:
        Column index (0-based) for valid input
    """
    cols = len(board[0])
    
    while True:
        user_input = input(f"Please enter a column (A-{chr(ord('A') + cols - 1)}): ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= cols:
            print(f"Invalid input. Please enter a column between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is not full
        if board[0][col] != ' ':
            print("That column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The current game board
        col: Column index (0-based)
        checker: The player's checker symbol
    
    Returns:
        True if placement was successful, False otherwise
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    
    return False


def check_win(board, checker):
    """
    Check if the specified checker has won the game.
    
    Args:
        board: The current game board
        checker: The player's checker symbol
    
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


def check_draw(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: The current game board
    
    Returns:
        True if the board is full, False otherwise
    """
    return all(board[0][col] != ' ' for col in range(len(board[0])))


def get_random_player(num_players):
    """
    Select a random starting player.
    
    Args:
        num_players: Number of players in the game
    
    Returns:
        Random player index (0-based)
    """
    return random.randint(0, num_players - 1)


def play_game(rows, cols, num_players):
    """
    Main game loop for Connect 4.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
        num_players: Number of players in the game
    """
    # Initialize the board
    board = initialize_board(rows, cols)
    
    # Select random starting player
    current_player = get_random_player(num_players)
    
    # Print initial board
    print_board(board)
    print(f"Starting player is: {CHECKERS[current_player]}\n")
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Get valid column from player
        print(f"Player {checker}, please enter a column:")
        col = get_valid_input(board, num_players)
        
        # Place the checker
        place_checker(board, col, checker)
        
        # Print updated board
        print_board(board)
        
        # Check if current player won
        if check_win(board, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check if the board is full (draw)
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % num_players


def main():
    """
    Main function to start the game.
    """
    play_game(ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
