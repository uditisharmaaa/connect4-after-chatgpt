import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Global Variables ---
board = []
current_player_index = 0

# --- Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates an empty game board with specified dimensions."""
    global board
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the game board to the console."""
    clear_screen()
    
    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:NUM_COLS]))
    
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

def get_column_input(player_checker):
    """
    Prompts the current player for column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            
            # Check if input is a single letter
            if len(col_char) != 1 or not 'A' <= col_char <= string.ascii_uppercase[NUM_COLS - 1]:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue
            
            col_index = ord(col_char) - ord('A')
            
            # Check if column is within bounds
            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column. Please choose a column between A and {string.ascii_uppercase[NUM_COLS - 1]}.")
                continue
            
            # Check if column is full
            if board[0][col_index] != " ":
                print("That column is full. Please choose another column.")
                continue
            
            return col_index
        
        except Exception:
            print("An unexpected error occurred. Please try again.")

def place_checker(col_index, player_checker):
    """
    Places the player's checker in the lowest available spot in the given column.
    Returns True if successful, False if the column is full (though this should be caught by validation).
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False # Should not be reached if validation is correct

def check_win(player_checker):
    """
    Checks if the current player has achieved a win condition (4 in a row).
    Checks horizontally, vertically, and diagonally.
    """
    
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True
                
    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == player_checker for i in range(WIN_CONDITION)):
                return True
                
    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True
                
    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True
                
    return False

def check_draw():
    """Checks if the board is completely full, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True # No empty spaces found

def main():
    """Main function to run the Connect 4 game."""
    global current_player_index
    
    create_board()
    
    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        
        print_board()
        
        col_index = get_column_input(current_player_checker)
        
        place_checker(col_index, current_player_checker)
        
        if check_win(current_player_checker):
            print_board()
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw():
            print_board()
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
