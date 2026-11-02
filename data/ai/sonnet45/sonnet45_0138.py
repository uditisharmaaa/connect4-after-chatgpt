import random
import os

# Constants for game configuration
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']


def create_board():
    """
    Creates and returns a new game board initialized with empty spaces.
    Returns a 2D list with ROWS rows and COLS columns.
    """
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
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
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print the board with borders
    for row in range(ROWS):
        # Print top border of each row
        print("+---" * COLS + "+")
        
        # Print the row content
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLS + "+")


def get_valid_column(board, player):
    """
    Prompts the player for a column input and validates it.
    Returns the column index (0-based) when valid input is received.
    """
    while True:
        user_input = input(f"Player {player}, please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Convert to uppercase
        user_input = user_input.upper()
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - 65
        
        # Check if column is within board range
        if col_index < 0 or col_index >= COLS:
            print("Invalid column. Please choose a column within the board.")
            continue
        
        # Check if column has space
        if board[0][col_index] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, player):
    """
    Places a checker in the specified column for the given player.
    The checker falls to the lowest available row.
    Returns the row index where the checker was placed, or -1 if column is full.
    """
    # Start from the bottom row and move up
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    
    return -1  # Column is full


def check_win(board, row, col, player):
    """
    Checks if the current player has won the game after placing a checker at (row, col).
    Checks horizontal, vertical, and both diagonal directions.
    Returns True if the player has won, False otherwise.
    """
    # Check horizontal
    if check_direction(board, row, col, player, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, player, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, player, 1, 1):
        return True
    
    # Check diagonal (bottom-left to top-right)
    if check_direction(board, row, col, player, -1, 1):
        return True
    
    return False


def check_direction(board, row, col, player, delta_row, delta_col):
    """
    Checks if there are WIN_LENGTH checkers in a row in a specific direction.
    delta_row and delta_col define the direction to check.
    Returns True if WIN_LENGTH consecutive checkers are found, False otherwise.
    """
    count = 1  # Count the current checker
    
    # Check in the positive direction
    count += count_consecutive(board, row, col, player, delta_row, delta_col)
    
    # Check in the negative direction
    count += count_consecutive(board, row, col, player, -delta_row, -delta_col)
    
    return count >= WIN_LENGTH


def count_consecutive(board, row, col, player, delta_row, delta_col):
    """
    Counts consecutive checkers of the same player in a specific direction.
    Returns the count of consecutive checkers (not including the starting position).
    """
    count = 0
    current_row = row + delta_row
    current_col = col + delta_col
    
    while (0 <= current_row < ROWS and 
           0 <= current_col < COLS and 
           board[current_row][current_col] == player):
        count += 1
        current_row += delta_row
        current_col += delta_col
    
    return count


def check_draw(board):
    """
    Checks if the board is full (game is a draw).
    Returns True if the board is full, False otherwise.
    """
    # Check if the top row has any empty spaces
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True


def main():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize the game board
    board = create_board()
    
    # Get player symbols based on number of players
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player = players[current_player_index]
        
        # Get valid column from player
        col = get_valid_column(board, current_player)
        
        # Place the checker
        row = place_checker(board, col, current_player)
        
        # Print the updated board
        print_board(board)
        
        # Check if the current player won
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        # Check if the game is a draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    main()
