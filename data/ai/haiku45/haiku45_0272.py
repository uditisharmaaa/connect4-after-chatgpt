import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, cols):
    """
    Create and initialize a 2D board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the Connect 4 board
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the current state of the board to the console.
    
    Args:
        board: The 2D board to print
    """
    os.system('clear')
    
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print board rows with separators
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * cols + "+")


def is_valid_column(column_letter, cols):
    """
    Check if the input column letter is valid.
    
    Args:
        column_letter: A single character representing a column
        cols: Number of columns in the board
    
    Returns:
        Column index if valid, -1 otherwise
    """
    if len(column_letter) != 1:
        return -1
    
    column_letter = column_letter.upper()
    
    if not column_letter.isalpha():
        return -1
    
    col_index = ord(column_letter) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index


def can_place_checker(board, col_index):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The current board state
        col_index: Index of the column
    
    Returns:
        True if a checker can be placed, False otherwise
    """
    rows = len(board)
    return board[0][col_index] == ' '


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column. The checker falls to the lowest
    available position in that column.
    
    Args:
        board: The current board state
        col_index: Index of the column
        checker: The checker symbol to place
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest empty row in this column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """
    Check if the last placed checker at (row, col) creates a winning configuration.
    Checks horizontally, vertically, and both diagonals.
    
    Args:
        board: The current board state
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal1, diagonal2
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely filled.
    
    Args:
        board: The current board state
    
    Returns:
        True if the board is full, False otherwise
    """
    cols = len(board[0])
    
    for col in range(cols):
        if board[0][col] == ' ':
            return False
    
    return True


def get_random_player(num_players):
    """
    Select a random starting player.
    
    Args:
        num_players: Number of players in the game
    
    Returns:
        Index of the randomly selected player (0-indexed)
    """
    return random.randint(0, num_players - 1)


def get_next_player(current_player, num_players):
    """
    Get the next player's index.
    
    Args:
        current_player: Index of the current player
        num_players: Total number of players
    
    Returns:
        Index of the next player
    """
    return (current_player + 1) % num_players


def play_game():
    """
    Main game loop for Connect 4.
    Handles initialization, turn alternation, input validation, win checking,
    and game state management.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Select a random starting player
    current_player = get_random_player(NUM_PLAYERS)
    
    # Get the checker symbols for all players
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Display initial board
    print_board(board)
    
    game_over = False
    winner = None
    
    # Main game loop
    while not game_over:
        checker = checkers[current_player]
        player_label = chr(65 + current_player) if NUM_PLAYERS > 2 else checker
        
        # Get player input
        valid_input = False
        while not valid_input:
            user_input = input(f"Player {checker}, please enter a column: ")
            col_index = is_valid_column(user_input, COLUMNS)
            
            if col_index == -1:
                print("Invalid input. Please enter a valid column letter (A-{}).".format(
                    chr(65 + COLUMNS - 1)))
                continue
            
            if not can_place_checker(board, col_index):
                print("Column is full. Please choose another column.")
                continue
            
            valid_input = True
        
        # Place the checker
        row = place_checker(board, col_index, checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, row, col_index, checker):
            print(f"Player {checker} won!")
            game_over = True
            winner = checker
        
        # Check for a draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        # Move to next player if game is not over
        if not game_over:
            current_player = get_next_player(current_player, NUM_PLAYERS)


def main():
    """
    Entry point for the Connect 4 game.
    """
    play_game()


if __name__ == "__main__":
    main()
