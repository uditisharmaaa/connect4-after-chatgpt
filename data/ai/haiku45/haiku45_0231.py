import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, columns):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board


def print_board(board, columns):
    """
    Print the current state of the game board.
    
    Args:
        board: The game board (2D list)
        columns: Number of columns in the board
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(columns):
        print(f" {chr(ord('A') + col)} ", end=" ")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(columns):
        print("---+", end="")
    print()
    
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        
        # Print row border
        print("+", end="")
        for _ in range(columns):
            print("---+", end="")
        print()


def is_valid_input(user_input, columns):
    """
    Validate user input for column selection.
    
    Args:
        user_input: The input string from the user
        columns: Number of columns in the board
    
    Returns:
        True if input is valid, False otherwise
    """
    if len(user_input) != 1:
        return False
    
    if not user_input.isupper():
        return False
    
    col_index = ord(user_input) - ord('A')
    
    if col_index < 0 or col_index >= columns:
        return False
    
    return True


def get_player_move(board, columns, player_checker):
    """
    Get valid move from the current player.
    
    Args:
        board: The game board (2D list)
        columns: Number of columns in the board
        player_checker: The checker symbol of the current player
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        
        if not is_valid_input(user_input, columns):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col_index, player_checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board (2D list)
        col_index: The column index (0-based) where the checker should be placed
        player_checker: The checker symbol of the current player
    
    Returns:
        True if checker was placed successfully, False otherwise
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            return True
    
    return False


def check_win(board, rows, columns, player_checker):
    """
    Check if the current player has won the game.
    
    Args:
        board: The game board (2D list)
        rows: Number of rows in the board
        columns: Number of columns in the board
        player_checker: The checker symbol of the current player
    
    Returns:
        True if the player has won, False otherwise
    """
    # Check horizontal
    for row in range(rows):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(columns):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, columns):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board, columns):
    """
    Check if the board is completely full.
    
    Args:
        board: The game board (2D list)
        columns: Number of columns in the board
    
    Returns:
        True if board is full, False otherwise
    """
    for col in range(columns):
        if board[0][col] == " ":
            return False
    return True


def get_next_player(current_player_index, num_players):
    """
    Get the index of the next player.
    
    Args:
        current_player_index: Index of the current player
        num_players: Total number of players
    
    Returns:
        Index of the next player
    """
    return (current_player_index + 1) % num_players


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLUMNS)
    
    # Main game loop
    while True:
        current_player_checker = CHECKERS[current_player_index]
        
        # Get player move
        col_index = get_player_move(board, COLUMNS, current_player_checker)
        
        # Place checker
        place_checker(board, col_index, current_player_checker)
        
        # Print updated board
        print_board(board, COLUMNS)
        
        # Check for win
        if check_win(board, ROWS, COLUMNS, current_player_checker):
            print(f"Player {current_player_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board, COLUMNS):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = get_next_player(current_player_index, NUM_PLAYERS)


if __name__ == "__main__":
    play_game()
