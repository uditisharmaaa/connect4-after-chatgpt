import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the game board with empty spaces.
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the current state of the board with column labels and formatting.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        # Print top border
        print("+---" * COLS + "+")
        
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLS + "+")


def get_player_symbol(player_index):
    """
    Get the checker symbol for a given player index.
    """
    return CHECKERS[player_index]


def is_valid_column(col_letter):
    """
    Check if the column letter is valid.
    Returns the column index (0-based) if valid, otherwise returns -1.
    """
    if len(col_letter) != 1:
        return -1
    
    col_letter = col_letter.upper()
    
    if not col_letter.isalpha():
        return -1
    
    col_index = ord(col_letter) - ord('A')
    
    if col_index < 0 or col_index >= COLS:
        return -1
    
    return col_index


def is_column_full(board, col_index):
    """
    Check if a column is completely filled.
    """
    return board[0][col_index] != " "


def get_available_row(board, col_index):
    """
    Get the row index where a checker should be placed in the given column.
    Returns the row index if space is available, otherwise returns -1.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            return row
    return -1


def place_checker(board, col_index, player_symbol):
    """
    Place a checker in the specified column.
    Returns True if successful, False otherwise.
    """
    row = get_available_row(board, col_index)
    
    if row == -1:
        return False
    
    board[row][col_index] = player_symbol
    return True


def get_player_input(current_player, player_symbol):
    """
    Get and validate player input for column selection.
    Keeps asking until valid input is received.
    """
    while True:
        try:
            col_letter = input(f"Player {player_symbol}, please enter a column: ")
            col_index = is_valid_column(col_letter)
            
            if col_index == -1:
                print("Invalid column. Please enter a valid column letter (A-{}).".format(
                    chr(65 + COLS - 1)))
                continue
            
            if is_column_full(board, col_index):
                print("This column is full. Please choose another column.")
                continue
            
            return col_index
        except Exception:
            print("Invalid input. Please try again.")


def check_direction(board, row, col, player_symbol, row_delta, col_delta):
    """
    Check if there are WIN_LENGTH checkers in a row starting from (row, col)
    in the direction specified by (row_delta, col_delta).
    """
    count = 0
    
    for i in range(WIN_LENGTH):
        r = row + i * row_delta
        c = col + i * col_delta
        
        if r < 0 or r >= ROWS or c < 0 or c >= COLS:
            return False
        
        if board[r][c] != player_symbol:
            return False
    
    return True


def check_win(board, row, col, player_symbol):
    """
    Check if the last placed checker at (row, col) results in a win.
    Checks horizontal, vertical, and both diagonal directions.
    """
    # Horizontal
    for start_col in range(max(0, col - WIN_LENGTH + 1), min(COLS - WIN_LENGTH + 1, col + 1)):
        if check_direction(board, row, start_col, player_symbol, 0, 1):
            return True
    
    # Vertical
    for start_row in range(max(0, row - WIN_LENGTH + 1), min(ROWS - WIN_LENGTH + 1, row + 1)):
        if check_direction(board, start_row, col, player_symbol, 1, 0):
            return True
    
    # Diagonal (top-left to bottom-right)
    for i in range(WIN_LENGTH):
        start_row = row - i
        start_col = col - i
        if start_row >= 0 and start_col >= 0 and start_row < ROWS and start_col < COLS:
            if check_direction(board, start_row, start_col, player_symbol, 1, 1):
                return True
    
    # Diagonal (top-right to bottom-left)
    for i in range(WIN_LENGTH):
        start_row = row - i
        start_col = col + i
        if start_row >= 0 and start_col < COLS and start_row < ROWS and start_col >= 0:
            if check_direction(board, start_row, start_col, player_symbol, 1, -1):
                return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely filled.
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """
    Main game loop.
    """
    board = initialize_board()
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    
    while not game_over:
        player_symbol = get_player_symbol(current_player)
        
        # Get valid player input
        col_index = get_player_input(current_player, player_symbol)
        
        # Place the checker
        row_index = get_available_row(board, col_index)
        place_checker(board, col_index, player_symbol)
        
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, player_symbol):
            print(f"Player {player_symbol} won!")
            game_over = True
        
        # Check for draw
        elif is_board_full(board):
            print("Draw! The board is full.")
            game_over = True
        
        else:
            # Switch to next player
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
