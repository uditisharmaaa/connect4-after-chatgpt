import os
import random

# Constants for board configuration
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Checkers for each player (up to 5 players)
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the game board with empty spaces.
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board


def print_board(board):
    """
    Print the current state of the board with column labels and grid lines.
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(BOARD_COLS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with grid lines
    for row in range(BOARD_ROWS):
        # Print top border
        print("+---" * BOARD_COLS + "+")
        
        # Print row content
        print("|", end="")
        for col in range(BOARD_COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * BOARD_COLS + "+")


def is_valid_input(column_letter, board):
    """
    Validate user input.
    Returns True if the input is valid (valid column letter and column not full),
    False otherwise.
    """
    # Check if input is a single character
    if len(column_letter) != 1:
        return False
    
    # Check if character is uppercase letter
    if not column_letter.isupper():
        return False
    
    # Check if character is within valid column range
    col_index = ord(column_letter) - ord('A')
    if col_index < 0 or col_index >= BOARD_COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True


def get_player_move(player_checker, board):
    """
    Get a valid move from the current player.
    Keeps asking until a valid input is provided.
    Returns the column index (0-based) where the checker should be placed.
    """
    while True:
        column_letter = input(f"Player {player_checker}, please enter a column: ")
        
        if is_valid_input(column_letter, board):
            col_index = ord(column_letter) - ord('A')
            return col_index
        else:
            print("Invalid input. Please enter a valid column letter (A-{}).".format(chr(65 + BOARD_COLS - 1)))


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available position.
    Returns the row index where the checker was placed.
    """
    # Start from the bottom and find the first empty space
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    # Column is full (should not happen due to input validation)
    return -1


def check_horizontal_win(board, row, col, checker):
    """
    Check if there are 4 checkers in a row horizontally starting from the given position.
    """
    count = 0
    # Check to the left and right from the current position
    for c in range(BOARD_COLS):
        if board[row][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    return False


def check_vertical_win(board, row, col, checker):
    """
    Check if there are 4 checkers in a row vertically starting from the given position.
    """
    count = 0
    # Check upwards and downwards from the current position
    for r in range(BOARD_ROWS):
        if board[r][col] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    return False


def check_diagonal_win(board, row, col, checker):
    """
    Check if there are 4 checkers in a row diagonally (both directions).
    """
    # Check diagonal from top-left to bottom-right
    # Find the starting point
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    
    count = 0
    r, c = start_row, start_col
    while r < BOARD_ROWS and c < BOARD_COLS:
        if board[r][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal from top-right to bottom-left
    start_row = row
    start_col = col
    while start_row > 0 and start_col < BOARD_COLS - 1:
        start_row -= 1
        start_col += 1
    
    count = 0
    r, c = start_row, start_col
    while r < BOARD_ROWS and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c -= 1
    
    return False


def check_win(board, row, col, checker):
    """
    Check if the current player has won after placing a checker at (row, col).
    Returns True if the player won, False otherwise.
    """
    if check_horizontal_win(board, row, col, checker):
        return True
    if check_vertical_win(board, row, col, checker):
        return True
    if check_diagonal_win(board, row, col, checker):
        return True
    return False


def check_draw(board):
    """
    Check if the board is full (draw condition).
    Returns True if all cells are filled, False otherwise.
    """
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True


def main():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board()
    
    # Choose a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get the current player's checker
        player_checker = CHECKERS[current_player]
        
        # Get player's move
        col_index = get_player_move(player_checker, board)
        
        # Place the checker
        row_index = place_checker(board, col_index, player_checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, player_checker):
            print(f"Player {player_checker} won!")
            game_over = True
        
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
