import os
import random

# Constants for board configuration
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers (in order)
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the game board with all cells set to empty spaces.
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the current state of the board to the console.
    Includes column labels and formatted grid.
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+---" * COLS + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
        print("+---" * COLS + "+")


def get_valid_input(board, current_player):
    """
    Get valid column input from the current player.
    Validates that the input is a valid column letter and the column is not full.
    Returns the column index (0-based).
    """
    while True:
        user_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        
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
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, current_player):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available row.
    Returns True if placement was successful, False otherwise.
    """
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = CHECKERS[current_player]
            return True
    
    return False


def check_horizontal_win(board, current_player):
    """
    Check if the current player has won with 4 in a row horizontally.
    Returns True if a win is found, False otherwise.
    """
    checker = CHECKERS[current_player]
    
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_vertical_win(board, current_player):
    """
    Check if the current player has won with 4 in a row vertically.
    Returns True if a win is found, False otherwise.
    """
    checker = CHECKERS[current_player]
    
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_diagonal_win(board, current_player):
    """
    Check if the current player has won with 4 in a row diagonally.
    Checks both diagonal directions (top-left to bottom-right and top-right to bottom-left).
    Returns True if a win is found, False otherwise.
    """
    checker = CHECKERS[current_player]
    
    # Check diagonal from top-left to bottom-right
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal from top-right to bottom-left
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, current_player):
    """
    Check if the current player has won the game.
    Checks all four directions: horizontal, vertical, and both diagonals.
    Returns True if a win is found, False otherwise.
    """
    return (check_horizontal_win(board, current_player) or
            check_vertical_win(board, current_player) or
            check_diagonal_win(board, current_player))


def check_draw(board):
    """
    Check if the board is completely full (draw condition).
    Returns True if the board is full, False otherwise.
    """
    return all(board[0][col] != " " for col in range(COLS))


def play_game():
    """
    Main game loop. Controls the flow of the Connect 4 game.
    """
    # Initialize the board
    board = initialize_board()
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Main game loop
    while True:
        # Get valid input from current player
        col = get_valid_input(board, current_player)
        
        # Place the checker
        place_checker(board, col, current_player)
        
        # Print the updated board
        print_board(board)
        
        # Check if current player has won
        if check_win(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        # Check if the board is full (draw)
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
