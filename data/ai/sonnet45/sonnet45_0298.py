import random
import os

# Constants for game configuration
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checker symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board():
    """
    Creates and returns an empty game board.
    Returns a 2D list with ROWS rows and COLS columns, initialized with spaces.
    """
    board = []
    for row in range(ROWS):
        board.append([" "] * COLS)
    return board


def print_board(board):
    """
    Prints the current state of the board with column labels.
    """
    # Clear the screen
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f"  {chr(65 + col)} ", end="")
    print()
    
    # Print the board with borders
    for row in range(ROWS):
        # Print top border of each row
        print("  ", end="")
        for col in range(COLS):
            print("+---", end="")
        print("+")
        
        # Print the row content
        print("  ", end="")
        for col in range(COLS):
            print(f"| {board[row][col]} ", end="")
        print("|")
    
    # Print bottom border
    print("  ", end="")
    for col in range(COLS):
        print("+---", end="")
    print("+")


def is_valid_column(board, col_letter):
    """
    Checks if the column input is valid.
    Returns the column index if valid, otherwise returns -1.
    """
    # Check if input is a single character
    if len(col_letter) != 1:
        return -1
    
    # Check if input is an uppercase letter
    if not col_letter.isupper():
        return -1
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column index is within board bounds
    if col_index < 0 or col_index >= COLS:
        return -1
    
    # Check if column has space (top row is not full)
    if board[0][col_index] != " ":
        return -1
    
    return col_index


def place_checker(board, col_index, symbol):
    """
    Places a checker in the specified column.
    Returns the row where the checker was placed, or -1 if column is full.
    """
    # Start from the bottom row and find the first empty cell
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return row
    return -1


def check_win(board, row, col, symbol):
    """
    Checks if placing a checker at (row, col) results in a win.
    Returns True if the player won, False otherwise.
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
    
    # Check diagonal (top-left to bottom-right)
    # Find the starting position of the diagonal
    start_row = row - min(row, col)
    start_col = col - min(row, col)
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
    
    # Check diagonal (bottom-left to top-right)
    # Find the starting position of the diagonal
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
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
    
    return False


def is_board_full(board):
    """
    Checks if the board is completely full.
    Returns True if full, False otherwise.
    """
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def play_game():
    """
    Main game loop that controls the flow of the game.
    """
    # Initialize the board
    board = create_board()
    
    # Get player symbols based on number of players
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_symbol = players[current_player_index]
        
        # Get valid input from current player
        valid_input = False
        while not valid_input:
            col_input = input(f"Player {current_symbol}, please enter a column: ")
            col_index = is_valid_column(board, col_input)
            
            if col_index == -1:
                print("Invalid input. Please try again.")
            else:
                valid_input = True
        
        # Place the checker
        row_placed = place_checker(board, col_index, current_symbol)
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, row_placed, col_index, current_symbol):
            print(f"Player {current_symbol} won!")
            game_over = True
        # Check for a draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Start the game
if __name__ == "__main__":
    play_game()
