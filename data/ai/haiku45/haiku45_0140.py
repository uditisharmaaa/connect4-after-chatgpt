import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
SYMBOLS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize a board with the given dimensions.
    All cells are initialized with whitespace.
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the board in the format specified in the assignment.
    """
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+---" * cols + "+")


def is_valid_column(column_letter, cols):
    """
    Check if the column letter is valid.
    Returns True if valid, False otherwise.
    """
    if len(column_letter) != 1:
        return False
    if not column_letter.isalpha():
        return False
    column_index = ord(column_letter.upper()) - ord('A')
    return 0 <= column_index < cols


def get_column_index(column_letter):
    """
    Convert column letter to column index.
    """
    return ord(column_letter.upper()) - ord('A')


def is_column_full(board, col_index):
    """
    Check if a column is completely full.
    """
    return board[0][col_index] != " "


def place_checker(board, col_index, symbol):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available position.
    Returns True if placement was successful, False if column is full.
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return True
    
    return False


def check_win(board, last_col, symbol):
    """
    Check if the last move resulted in a win.
    Returns True if there are 4 in a row, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])
    
    # Find the row where the symbol was just placed
    last_row = -1
    for row in range(rows):
        if board[row][last_col] == symbol:
            last_row = row
            break
    
    if last_row == -1:
        return False
    
    # Check horizontal
    if check_direction(board, last_row, last_col, symbol, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, last_row, last_col, symbol, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, last_row, last_col, symbol, 1, 1):
        return True
    
    # Check diagonal (top-right to bottom-left)
    if check_direction(board, last_row, last_col, symbol, 1, -1):
        return True
    
    return False


def check_direction(board, row, col, symbol, row_delta, col_delta):
    """
    Check if there are 4 symbols in a row in the specified direction.
    """
    rows = len(board)
    cols = len(board[0])
    count = 1
    
    # Check in positive direction
    r, c = row + row_delta, col + col_delta
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r += row_delta
        c += col_delta
    
    # Check in negative direction
    r, c = row - row_delta, col - col_delta
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r -= row_delta
        c -= col_delta
    
    return count >= WIN_LENGTH


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_player_move(player_symbol, cols):
    """
    Get a valid move from the current player.
    Keeps asking until a valid move is provided.
    """
    while True:
        move = input(f"Player {player_symbol}, please enter a column: ")
        
        # Check if input is valid
        if not is_valid_column(move, cols):
            print("Invalid input. Please enter a valid column letter (A-" + 
                  chr(ord('A') + cols - 1) + ").")
            continue
        
        col_index = get_column_index(move)
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def play_game(board, num_players, rows, cols):
    """
    Main game loop.
    """
    # Initialize game state
    current_player_index = random.randint(0, num_players - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's symbol
        current_symbol = SYMBOLS[current_player_index]
        
        # Get player's move
        col_index = get_player_move(current_symbol, cols)
        
        # Place checker
        place_checker(board, col_index, current_symbol)
        
        # Print board
        print_board(board)
        
        # Check for win
        if check_win(board, col_index, current_symbol):
            print(f"Player {current_symbol} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % num_players


def main():
    """
    Main function to start the game.
    """
    # Create and initialize board
    board = initialize_board(ROWS, COLS)
    
    # Start the game
    play_game(board, NUM_PLAYERS, ROWS, COLS)


if __name__ == "__main__":
    main()
