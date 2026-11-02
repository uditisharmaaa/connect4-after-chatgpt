import os
import random

# Constants for the game
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """
    Initialize the game board with empty spaces.
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    """
    Print the current state of the board with column labels and formatting.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLUMNS):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print_border()
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
        print_border()

def print_border():
    """
    Print the horizontal border of the board.
    """
    for _ in range(COLUMNS):
        print("+---", end="")
    print("+")

def get_valid_input(current_player_checker):
    """
    Get and validate user input for the column choice.
    Returns the column index (0-based) or -1 if input is invalid.
    """
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column index is within board range
        if col_index < 0 or col_index >= COLUMNS:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + COLUMNS - 1)}.")
            continue
        
        return col_index

def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column at the lowest available row.
    Returns True if placement was successful, False if column is full.
    """
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    # Column is full
    print("Column is full. Please choose another column.")
    return False

def check_win(board, row, col, checker):
    """
    Check if the last placed checker at (row, col) creates a win.
    Returns True if there are 4 checkers in a row, False otherwise.
    """
    # Directions: horizontal, vertical, diagonal-right, diagonal-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        # If 4 or more in a row, player wins
        if count >= WIN_LENGTH:
            return True
    
    return False

def check_draw(board):
    """
    Check if the board is completely filled (draw condition).
    Returns True if board is full, False otherwise.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def get_next_player(current_player_index):
    """
    Get the index of the next player.
    """
    return (current_player_index + 1) % NUM_PLAYERS

def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board()
    
    # Get player checkers based on number of players
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_checker = checkers[current_player_index]
        
        # Get valid column input
        col_index = get_valid_input(current_checker)
        
        # Try to place the checker
        if place_checker(board, col_index, current_checker):
            # Print updated board
            print_board(board)
            
            # Check for win
            # Find the row where the checker was placed
            for row in range(ROWS):
                if board[row][col_index] == current_checker:
                    placed_row = row
                    break
            
            if check_win(board, placed_row, col_index, current_checker):
                print(f"Player {current_checker} won!")
                game_over = True
            elif check_draw(board):
                print("The game is a draw!")
                game_over = True
            else:
                # Move to next player
                current_player_index = get_next_player(current_player_index)

def main():
    """
    Main entry point for the game.
    """
    play_game()

if __name__ == "__main__":
    main()
