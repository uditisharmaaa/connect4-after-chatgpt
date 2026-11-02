import os
import random

# Constants for board dimensions and players
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board():
    """
    Initialize the game board with all empty cells.
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the current state of the board to the console.
    Includes column labels and formatted grid.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLUMNS):
        print(f" {chr(ord('A') + col)}  ", end="")
    print()
    
    # Print board rows
    for row in range(ROWS):
        print("+---" * COLUMNS + "+")
        print("|", end="")
        for col in range(COLUMNS):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * COLUMNS + "+")


def get_player_input(current_player_checker):
    """
    Get and validate user input for column selection.
    Returns the column index (0-based) or None if invalid.
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
            print(f"Invalid column. Please enter a column between A and {chr(ord('A') + COLUMNS - 1)}.")
            continue
        
        return col_index


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available position.
    Returns True if placement was successful, False if column is full.
    """
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    # Column is full
    print("Column is full. Please choose another column.")
    return False


def check_win(board, checker):
    """
    Check if the specified checker has won the game.
    Returns True if the checker has 4 in a row, False otherwise.
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Check if the board is full (draw condition).
    Returns True if all cells are filled, False otherwise.
    """
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize board
    board = initialize_board()
    
    # Get list of player checkers
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_won = False
    
    while not game_won:
        current_checker = player_checkers[current_player_index]
        
        # Get valid column input from player
        valid_move = False
        while not valid_move:
            col_index = get_player_input(current_checker)
            valid_move = place_checker(board, col_index, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_won = True
        # Check for draw
        elif check_draw(board):
            print("Game is a draw!")
            game_won = True
        # Move to next player
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Entry point for the Connect 4 game.
    """
    play_game()


if __name__ == "__main__":
    main()
