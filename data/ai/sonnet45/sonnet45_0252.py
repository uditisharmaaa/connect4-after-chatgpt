import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
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

def get_column_input(player_symbol):
    """Get and return valid column input from player."""
    prompt = f"Player {player_symbol}, please enter a column: "
    user_input = input(prompt).strip().upper()
    return user_input

def is_valid_column(user_input):
    """Check if the input is a valid column letter."""
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    col_index = ord(user_input) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    return True

def is_column_available(board, col_index):
    """Check if the column has space for a checker."""
    return board[0][col_index] == " "

def place_checker(board, col_index, player_symbol):
    """Place the checker in the lowest available row of the column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_symbol
            return row
    return -1

def check_win(board, row, col, player_symbol):
    """Check if the last move resulted in a win."""
    # Check horizontal
    if check_direction(board, row, col, player_symbol, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, player_symbol, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, player_symbol, 1, 1):
        return True
    
    # Check diagonal (bottom-left to top-right)
    if check_direction(board, row, col, player_symbol, -1, 1):
        return True
    
    return False

def check_direction(board, row, col, player_symbol, delta_row, delta_col):
    """Check if there are 4 in a row in a specific direction."""
    count = 1  # Count the current position
    
    # Check in positive direction
    count += count_in_direction(board, row, col, player_symbol, delta_row, delta_col)
    
    # Check in negative direction
    count += count_in_direction(board, row, col, player_symbol, -delta_row, -delta_col)
    
    return count >= WIN_LENGTH

def count_in_direction(board, row, col, player_symbol, delta_row, delta_col):
    """Count consecutive checkers in a given direction."""
    count = 0
    current_row = row + delta_row
    current_col = col + delta_col
    
    while (0 <= current_row < ROWS and 
           0 <= current_col < COLS and 
           board[current_row][current_col] == player_symbol):
        count += 1
        current_row += delta_row
        current_col += delta_col
    
    return count

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
            user_input = get_column_input(current_player)
            
            # Validate input
            if not is_valid_column(user_input):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_index = ord(user_input) - 65
            
            # Check if column is available
            if not is_column_available(board, col_index):
                print("Column is full. You lose your turn.")
                valid_move = True
                break
            
            # Place checker
            row = place_checker(board, col_index, current_player)
            
            # Print updated board
            print_board(board)
            
            # Check for win
            if check_win(board, row, col_index, current_player):
                print(f"Player {current_player} won!")
                game_over = True
            # Check for draw
            elif is_board_full(board):
                print("The game is a draw!")
                game_over = True
            
            valid_move = True
        
        # Move to next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
