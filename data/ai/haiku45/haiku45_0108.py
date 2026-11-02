import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    """
    Create a new board with the specified dimensions.
    All cells are initialized with whitespace.
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the board to the console with proper formatting.
    """
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)} ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Top border
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()
        
        # Row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Bottom border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()


def is_valid_input(user_input, cols):
    """
    Check if the user input is valid.
    Valid input is a single uppercase letter within board range.
    """
    if len(user_input) != 1:
        return False
    
    if not user_input.isupper():
        return False
    
    if not user_input.isalpha():
        return False
    
    col_index = ord(user_input) - ord('A')
    if col_index < 0 or col_index >= cols:
        return False
    
    return True


def get_player_move(board, current_player_checker):
    """
    Get a valid move from the current player.
    Keep asking until valid input is received.
    """
    cols = len(board[0])
    
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        
        if not is_valid_input(user_input, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available position.
    Returns True if placement was successful, False otherwise.
    """
    rows = len(board)
    
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_horizontal_win(board, rows, cols, checker):
    """
    Check if there's a horizontal win for the given checker.
    """
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, rows, cols, checker):
    """
    Check if there's a vertical win for the given checker.
    """
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, rows, cols, checker):
    """
    Check if there's a diagonal win for the given checker.
    Checks both directions: top-left to bottom-right and top-right to bottom-left.
    """
    # Top-left to bottom-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Top-right to bottom-left
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker):
    """
    Check if the current player has won.
    """
    rows = len(board)
    cols = len(board[0])
    
    if check_horizontal_win(board, rows, cols, checker):
        return True
    
    if check_vertical_win(board, rows, cols, checker):
        return True
    
    if check_diagonal_win(board, rows, cols, checker):
        return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    """
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    
    return True


def play_game():
    """
    Main game loop. Controls the flow of the game.
    """
    # Create and initialize the board
    board = create_board(ROWS, COLS)
    
    # Get list of player checkers
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player_checker = player_checkers[current_player_index]
        
        # Get player move
        col = get_player_move(board, current_player_checker)
        
        # Place checker on board
        place_checker(board, col, current_player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("Draw! The board is full.")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
