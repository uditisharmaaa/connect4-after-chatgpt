import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def initialize_board():
    """
    Initialize the game board with empty spaces.
    
    Returns:
        A 2D list representing the board with dimensions ROWS x COLS.
    """
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """
    Print the current state of the board to the console.
    
    Args:
        board: The 2D list representing the game board.
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print top border
    print("+---" * COLS + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * COLS + "+")

def is_valid_move(board, col):
    """
    Check if a move in the given column is valid.
    
    Args:
        board: The 2D list representing the game board.
        col: The column index (0-based).
    
    Returns:
        True if the move is valid, False otherwise.
    """
    # Check if column is within bounds
    if col < 0 or col >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col] != " ":
        return False
    
    return True

def get_player_move(board, player_checker):
    """
    Get a valid move from the player.
    
    Args:
        board: The 2D list representing the game board.
        player_checker: The checker symbol of the current player.
    
    Returns:
        The column index (0-based) where the player wants to place their checker.
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col = ord(user_input) - ord('A')
        
        if not is_valid_move(board, col):
            print("Invalid column. Column is either out of range or full.")
            continue
        
        return col

def place_checker(board, col, checker):
    """
    Place a checker in the given column. The checker falls to the lowest available position.
    
    Args:
        board: The 2D list representing the game board.
        col: The column index (0-based).
        checker: The checker symbol to place.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            break

def check_win(board, checker):
    """
    Check if the given checker has won the game.
    
    Args:
        board: The 2D list representing the game board.
        checker: The checker symbol to check for a win.
    
    Returns:
        True if the checker has 4 in a row, False otherwise.
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The 2D list representing the game board.
    
    Returns:
        True if the board is full, False otherwise.
    """
    for row in board:
        if " " in row:
            return False
    return True

def get_player_checkers(num_players):
    """
    Get the list of checkers for the given number of players.
    
    Args:
        num_players: The number of players.
    
    Returns:
        A list of checker symbols for each player.
    """
    return CHECKERS[:num_players]

def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board()
    
    # Get player checkers
    player_checkers = get_player_checkers(NUM_PLAYERS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    game_won = False
    
    while not game_won:
        # Get current player's checker
        current_checker = player_checkers[current_player_index]
        
        # Get player's move
        col = get_player_move(board, current_checker)
        
        # Place the checker
        place_checker(board, col, current_checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_won = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_won = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """
    Entry point of the program.
    """
    play_game()

if __name__ == "__main__":
    main()
