import random
import os

# Global constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """
    Creates and returns an empty board as a 2D list.
    All cells are initialized with spaces.
    """
    board = []
    for row in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    """
    Prints the board with column labels (A, B, C, etc.) and borders.
    Clears the screen before printing.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        # Print top border of each cell
        print("+---" * COLS + "+")
        # Print cell contents
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLS + "+")

def is_valid_column(col_letter, board):
    """
    Checks if the input column letter is valid.
    Returns True if valid, False otherwise.
    """
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not col_letter.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column index is within board boundaries
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column has available space (top row not filled)
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, col_letter, player_symbol):
    """
    Places a checker in the specified column.
    The checker falls to the lowest available position.
    Returns True if successful, False otherwise.
    """
    col_index = ord(col_letter) - 65
    
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_symbol
            return True
    
    return False

def check_win(board, player_symbol):
    """
    Checks if the player with the given symbol has won.
    Checks horizontal, vertical, and diagonal (both directions) for 4 in a row.
    Returns True if the player has won, False otherwise.
    """
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player_symbol and
                board[row][col + 1] == player_symbol and
                board[row][col + 2] == player_symbol and
                board[row][col + 3] == player_symbol):
                return True
    
    # Check vertical wins
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player_symbol and
                board[row + 1][col] == player_symbol and
                board[row + 2][col] == player_symbol and
                board[row + 3][col] == player_symbol):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player_symbol and
                board[row + 1][col + 1] == player_symbol and
                board[row + 2][col + 2] == player_symbol and
                board[row + 3][col + 3] == player_symbol):
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player_symbol and
                board[row - 1][col + 1] == player_symbol and
                board[row - 2][col + 2] == player_symbol and
                board[row - 3][col + 3] == player_symbol):
                return True
    
    return False

def check_draw(board):
    """
    Checks if the board is full (draw condition).
    Returns True if board is full, False otherwise.
    """
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def main():
    """
    Main game loop for Connect 4.
    """
    # Create the board
    board = create_board()
    
    # Select players for the game
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player = players[current_player_index]
        
        # Get player input
        valid_input = False
        while not valid_input:
            col_input = input(f"Player {current_player}, please enter a column: ")
            
            if is_valid_column(col_input, board):
                valid_input = True
            else:
                print("Invalid input. Please enter a valid column letter.")
        
        # Place the checker
        place_checker(board, col_input, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
