import os
import random

# Configuration constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board(rows, columns):
    """
    Initialize a board with all empty spaces.
    
    Args:
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        A 2D list representing the board with all spaces empty
    """
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board


def print_board(board, columns):
    """
    Print the current state of the board with column labels and grid.
    
    Args:
        board: The 2D list representing the board
        columns: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(columns):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print top border
    print("+---" * columns + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * columns + "+")


def is_valid_column(column_letter, columns):
    """
    Check if the input column letter is valid.
    
    Args:
        column_letter: The letter entered by the player
        columns: Number of columns in the board
    
    Returns:
        True if valid, False otherwise
    """
    if len(column_letter) != 1:
        return False
    
    if not column_letter.isalpha():
        return False
    
    column_letter = column_letter.upper()
    column_index = ord(column_letter) - ord('A')
    
    if column_index < 0 or column_index >= columns:
        return False
    
    return True


def get_column_index(column_letter):
    """
    Convert a column letter to its index.
    
    Args:
        column_letter: The letter entered by the player
    
    Returns:
        The index of the column
    """
    return ord(column_letter.upper()) - ord('A')


def can_place_checker(board, column_index, rows):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The 2D list representing the board
        column_index: The index of the column
        rows: Number of rows in the board
    
    Returns:
        True if a checker can be placed, False otherwise
    """
    return board[0][column_index] == " "


def place_checker(board, column_index, player_checker, rows):
    """
    Place a checker in the given column.
    
    Args:
        board: The 2D list representing the board
        column_index: The index of the column
        player_checker: The checker symbol of the player
        rows: Number of rows in the board
    
    Returns:
        The row index where the checker was placed
    """
    for row in range(rows - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = player_checker
            return row
    
    return -1


def check_win_direction(board, row, col, player_checker, rows, columns, row_delta, col_delta):
    """
    Check if a player has won by looking in a specific direction from a position.
    
    Args:
        board: The 2D list representing the board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        player_checker: The checker symbol of the player
        rows: Number of rows in the board
        columns: Number of columns in the board
        row_delta: The direction to check vertically (-1, 0, or 1)
        col_delta: The direction to check horizontally (-1, 0, or 1)
    
    Returns:
        True if the player has won in this direction, False otherwise
    """
    count = 1  # Count the current checker
    
    # Check in the positive direction
    r, c = row + row_delta, col + col_delta
    while 0 <= r < rows and 0 <= c < columns and board[r][c] == player_checker:
        count += 1
        r += row_delta
        c += col_delta
    
    # Check in the negative direction
    r, c = row - row_delta, col - col_delta
    while 0 <= r < rows and 0 <= c < columns and board[r][c] == player_checker:
        count += 1
        r -= row_delta
        c -= col_delta
    
    return count >= WIN_LENGTH


def check_win(board, row, col, player_checker, rows, columns):
    """
    Check if the current player has won the game.
    
    Args:
        board: The 2D list representing the board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        player_checker: The checker symbol of the player
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        True if the player has won, False otherwise
    """
    # Check horizontal
    if check_win_direction(board, row, col, player_checker, rows, columns, 0, 1):
        return True
    
    # Check vertical
    if check_win_direction(board, row, col, player_checker, rows, columns, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_win_direction(board, row, col, player_checker, rows, columns, 1, 1):
        return True
    
    # Check diagonal (top-right to bottom-left)
    if check_win_direction(board, row, col, player_checker, rows, columns, 1, -1):
        return True
    
    return False


def is_board_full(board, rows, columns):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The 2D list representing the board
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        True if the board is full, False otherwise
    """
    for col in range(columns):
        if board[0][col] == " ":
            return False
    
    return True


def play_game(rows, columns, num_players):
    """
    Main game loop for Connect 4.
    
    Args:
        rows: Number of rows in the board
        columns: Number of columns in the board
        num_players: Number of players in the game
    """
    # Initialize the board
    board = initialize_board(rows, columns)
    
    # Select random first player
    current_player_index = random.randint(0, num_players - 1)
    
    # Print initial board
    print_board(board, columns)
    
    # Game loop
    game_over = False
    
    while not game_over:
        player_checker = CHECKERS[current_player_index]
        player_name = chr(ord('A') + current_player_index) if current_player_index > 0 else "X" if current_player_index == 0 else "O"
        player_name = player_checker
        
        # Get valid input from player
        valid_input = False
        while not valid_input:
            column_letter = input(f"Player {player_name}, please enter a column: ")
            
            # Validate column letter
            if not is_valid_column(column_letter, columns):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            column_index = get_column_index(column_letter)
            
            # Check if column is not full
            if not can_place_checker(board, column_index, rows):
                print("Column is full. Please choose another column.")
                continue
            
            valid_input = True
        
        # Place the checker
        row = place_checker(board, column_index, player_checker, rows)
        
        # Print the board
        print_board(board, columns)
        
        # Check for win
        if check_win(board, row, column_index, player_checker, rows, columns):
            print(f"Player {player_name} won!")
            game_over = True
        
        # Check for draw
        elif is_board_full(board, rows, columns):
            print("It's a draw!")
            game_over = True
        
        # Move to next player
        if not game_over:
            current_player_index = (current_player_index + 1) % num_players


def main():
    """
    Main function to start the Connect 4 game.
    """
    play_game(ROWS, COLUMNS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
