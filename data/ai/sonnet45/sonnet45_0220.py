import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board():
    """Create and return an empty board with ROWS x COLS dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+" + "---+" * COLS)


def get_player_input(player_symbol):
    """Get and return the column choice from the player."""
    column = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
    return column


def is_valid_column(column):
    """Check if the column input is valid (A-G for default 7 columns)."""
    if len(column) != 1:
        return False
    if not column.isalpha():
        return False
    col_index = ord(column) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    return True


def is_column_available(board, col_index):
    """Check if the column has space available."""
    return board[0][col_index] == " "


def place_checker(board, col_index, player_symbol):
    """Place the checker in the specified column. Returns True if successful."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_symbol
            return True
    return False


def check_win(board, player_symbol):
    """Check if the player has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            if all(board[row + i][col] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Set up players
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player = players[current_player_index]
        
        # Get valid input from player
        valid_move = False
        while not valid_move:
            column_input = get_player_input(current_player)
            
            # Validate input
            if not is_valid_column(column_input):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_index = ord(column_input) - 65
            
            # Check if column is available
            if not is_column_available(board, col_index):
                print("Column is full. You lose your turn.")
                valid_move = True
                break
            
            # Place the checker
            if place_checker(board, col_index, current_player):
                valid_move = True
            else:
                print("Could not place checker. Try again.")
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            game_over = True
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
