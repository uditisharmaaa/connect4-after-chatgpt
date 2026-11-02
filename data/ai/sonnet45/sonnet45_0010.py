import random
import os

# Global constants for game configuration
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board():
    """
    Creates and returns an empty game board.
    The board is a 2D list with ROWS rows and COLS columns.
    All cells are initialized with spaces.
    """
    board = []
    for row in range(ROWS):
        board.append([" "] * COLS)
    return board


def print_board(board):
    """
    Prints the current state of the board with column labels.
    Clears the screen before printing.
    """
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f"  {chr(65 + col)} ", end="")
    print()
    
    # Print separator line
    print("  +" + "---+" * COLS)
    
    # Print each row
    for row in range(ROWS):
        print("  |", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
        print("  +" + "---+" * COLS)


def is_valid_move(board, col):
    """
    Checks if a move to the specified column is valid.
    A move is valid if the column is not full (top row has space).
    """
    return board[0][col] == " "


def place_checker(board, col, symbol):
    """
    Places a checker in the specified column.
    The checker falls to the lowest available row in that column.
    Returns the row where the checker was placed, or -1 if invalid.
    """
    # Start from the bottom row and work upward
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row
    return -1


def check_win(board, row, col, symbol):
    """
    Checks if placing a checker at (row, col) creates a win for the given symbol.
    Checks horizontal, vertical, and both diagonal directions.
    """
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    # Find the starting position of the diagonal
    start_row = row
    start_col = col
    while start_row < ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    
    count = 0
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    # Find the starting position of the diagonal
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    
    count = 0
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    return False


def is_board_full(board):
    """
    Checks if the board is completely full (draw condition).
    Returns True if no empty spaces exist in the top row.
    """
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def get_player_move(board, player_symbol):
    """
    Prompts the current player for a move and validates the input.
    Returns the column index (0-based) of the valid move.
    """
    while True:
        move = input(f"Player {player_symbol}, please enter a column: ")
        
        # Check if input is a single character
        if len(move) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Convert to uppercase
        move = move.upper()
        
        # Check if input is a letter
        if not move.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(move) - 65
        
        # Check if column is within board range
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(64 + COLS)}.")
            continue
        
        # Check if column is not full
        if not is_valid_move(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize the board
    board = create_board()
    
    # Get player symbols based on number of players
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's symbol
        current_symbol = players[current_player_index]
        
        # Get player's move
        col = get_player_move(board, current_symbol)
        
        # Place the checker
        row = place_checker(board, col, current_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            print(f"Player {current_symbol} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Main entry point
if __name__ == "__main__":
    play_game()
