import os
import random

# Constants for board dimensions and game settings
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Checker symbols for each player (up to 5 players)
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the board with empty spaces (whitespaces).
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the board with column labels and grid formatting.
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(COLS):
        print("---+", end="")
    print()
    
    # Print each row
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
        
        # Print horizontal border after each row
        print("+", end="")
        for _ in range(COLS):
            print("---+", end="")
        print()


def get_next_empty_row(board, col):
    """
    Find the next empty row in the given column.
    Returns the row index if a space is available, otherwise returns -1.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


def is_valid_move(board, col):
    """
    Check if a move is valid (column exists and has space).
    Returns True if valid, False otherwise.
    """
    if col < 0 or col >= COLS:
        return False
    if get_next_empty_row(board, col) == -1:
        return False
    return True


def get_player_move(board, player_checker):
    """
    Get valid input from the player.
    Keeps asking until a valid column is provided.
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input format
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter (A-{}).".format(chr(65 + COLS - 1)))
            continue
        
        # Convert letter to column index
        col = ord(user_input) - 65
        
        # Check if column is within bounds
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Check if column has space
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, player_checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available row.
    """
    row = get_next_empty_row(board, col)
    if row != -1:
        board[row][col] = player_checker


def check_horizontal_win(board, player_checker):
    """
    Check if the player has won horizontally.
    """
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, player_checker):
    """
    Check if the player has won vertically.
    """
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, player_checker):
    """
    Check if the player has won diagonally.
    Checks both directions: bottom-left to top-right and top-left to bottom-right.
    """
    # Check bottom-left to top-right diagonals
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check top-left to bottom-right diagonals
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, player_checker):
    """
    Check if the current player has won.
    Returns True if player has 4 in a row, False otherwise.
    """
    return (check_horizontal_win(board, player_checker) or
            check_vertical_win(board, player_checker) or
            check_diagonal_win(board, player_checker))


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board()
    
    # Select a random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player_index]
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    while True:
        # Get the player's move
        col = get_player_move(board, current_checker)
        
        # Place the checker
        place_checker(board, col, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check if current player won
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check if board is full (draw)
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_checker = CHECKERS[current_player_index]


# Main entry point
if __name__ == "__main__":
    play_game()
