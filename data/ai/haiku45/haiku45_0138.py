import os
import random

# Constants for board configuration
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the game board with all empty spaces.
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the current state of the board to the console.
    Includes column labels and formatting.
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLUMNS):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(COLUMNS):
        print("---+", end="")
    print()
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for _ in range(COLUMNS):
            print("---+", end="")
        print()


def get_column_input(current_player_checker):
    """
    Get valid column input from the player.
    Keeps asking until a valid input is provided.
    Returns the column index (0-based).
    """
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= COLUMNS:
            print(f"Invalid input. Please enter a column between A and {chr(ord('A') + COLUMNS - 1)}.")
            continue
        
        return col_index


def is_column_full(board, col):
    """
    Check if a column is completely filled.
    Returns True if full, False otherwise.
    """
    return board[0][col] != " "


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available row.
    Returns True if placement was successful, False if column is full.
    """
    if is_column_full(board, col):
        return False
    
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_horizontal_win(board, checker):
    """
    Check if the player with the given checker has won horizontally.
    Returns True if there are 4 checkers in a row horizontally.
    """
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, checker):
    """
    Check if the player with the given checker has won vertically.
    Returns True if there are 4 checkers in a row vertically.
    """
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, checker):
    """
    Check if the player with the given checker has won diagonally.
    Checks both directions: bottom-left to top-right and bottom-right to top-left.
    Returns True if there are 4 checkers in a row diagonally.
    """
    # Check diagonal from bottom-left to top-right direction
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal from bottom-right to top-left direction
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker):
    """
    Check if the player with the given checker has won.
    Returns True if the player has won, False otherwise.
    """
    return (check_horizontal_win(board, checker) or 
            check_vertical_win(board, checker) or 
            check_diagonal_win(board, checker))


def is_board_full(board):
    """
    Check if the board is completely filled.
    Returns True if the board is full, False otherwise.
    """
    return all(board[0][col] != " " for col in range(COLUMNS))


def get_current_player_checker(current_player_index):
    """
    Get the checker symbol for the current player.
    """
    return CHECKERS[current_player_index]


def play_game():
    """
    Main game loop. Handles the flow of the game from initialization to completion.
    """
    # Initialize the board
    board = initialize_board()
    
    # Randomly select the starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    game_over = False
    
    # Main game loop
    while not game_over:
        current_checker = get_current_player_checker(current_player)
        
        # Get valid column input from player
        col = get_column_input(current_checker)
        
        # Try to place the checker
        if not place_checker(board, col, current_checker):
            print("Column is full. Turn lost.")
            print_board(board)
        else:
            # Print updated board
            print_board(board)
            
            # Check if current player has won
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                game_over = True
            # Check if the board is full (draw)
            elif is_board_full(board):
                print("It's a draw!")
                game_over = True
            else:
                # Move to next player
                current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """
    Entry point for the game.
    """
    play_game()


if __name__ == "__main__":
    main()
