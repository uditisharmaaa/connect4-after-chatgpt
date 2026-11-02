import os
import random

# Constants
BOARD_COLS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board():
    """
    Initialize the game board with empty spaces.
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board


def print_board(board):
    """
    Print the game board with column labels and formatting.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(BOARD_COLS):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(BOARD_COLS):
        print("---+", end="")
    print()
    
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        
        # Print bottom border
        print("+", end="")
        for _ in range(BOARD_COLS):
            print("---+", end="")
        print()


def get_valid_input(current_player):
    """
    Get valid column input from the player.
    Returns the column index (0-based).
    """
    while True:
        try:
            user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
            
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
            
            # Check if column index is within bounds
            if col_index < 0 or col_index >= BOARD_COLS:
                print(f"Invalid column. Please enter a letter between A and {chr(65 + BOARD_COLS - 1)}.")
                continue
            
            return col_index
        
        except Exception:
            print("Invalid input. Please try again.")


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    Returns True if placement was successful, False if column is full.
    """
    # Find the lowest empty row in the column
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    # Column is full
    print("Column is full. Please choose another column.")
    return False


def check_win(board, checker):
    """
    Check if the specified checker has won.
    Returns True if the checker has 4 in a row, False otherwise.
    """
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - WIN_LENGTH + 1):
        for col in range(BOARD_COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(BOARD_ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, BOARD_COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Check if the board is full (draw condition).
    Returns True if board is full, False otherwise.
    """
    for row in board:
        if " " in row:
            return False
    return True


def main():
    """
    Main game loop for Connect 4.
    """
    # Initialize board
    board = initialize_board()
    
    # Get list of players with their checkers
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player = players[current_player_index]
        
        # Get valid column input
        col_index = get_valid_input(current_player)
        
        # Try to place checker
        if not place_checker(board, col_index, current_player):
            # Invalid placement (column full), ask for input again
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
