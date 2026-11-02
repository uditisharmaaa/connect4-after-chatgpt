import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Global Variables ---
board = []
current_player_index = 0

# --- Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Initializes the game board with empty spaces."""
    global board
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()
    
    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:NUM_COLS]))
    
    # Print board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or col_char not in string.ascii_uppercase[:NUM_COLS]:
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C).")
                continue
            
            col = ord(col_char) - ord('A')
            
            # Check if column is full
            if board[0][col] != ' ':
                print(f"Column {col_char} is full. Please choose another column.")
                continue
                
            return col
        except Exception:
            print("Invalid input. Please enter a valid column letter.")

def drop_checker(col, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if successful, False if the column is full (shouldn't happen with validation).
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = player_checker
            return True
    return False # Should not be reached due to prior validation

def check_win(player_checker):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    # Helper function to check a line
    def check_line(r_start, c_start, r_dir, c_dir):
        count = 0
        for i in range(WIN_CONDITION):
            r, c = r_start + i * r_dir, c_start + i * c_dir
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
                count += 1
            else:
                return False
        return True

    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if check_line(r, c, 0, 1):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
            if check_line(r, c, 1, 0):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if check_line(r, c, 1, 1):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if check_line(r, c, -1, 1):
                return True

    return False

def check_draw():
    """Checks if the board is completely full (a draw)."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False
    return True

def switch_player():
    """Switches the current player to the next one."""
    global current_player_index
    current_player_index = (current_player_index + 1) % NUM_PLAYERS

def play_game():
    """Main function to run the Connect 4 game."""
    global current_player_index

    create_board()
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    winner = None
    game_over = False

    while not game_over:
        print_board()
        current_player_checker = CHECKERS[current_player_index]

        col_index = get_column_input(current_player_checker)
        
        drop_successful = drop_checker(col_index, current_player_checker)
        
        # This conditional is mostly for robustness, get_column_input should prevent False
        if not drop_successful:
            print(f"Error: Column {string.ascii_uppercase[col_index]} was unexpectedly full. Skipping turn.")
            switch_player() # Player loses turn if this happens
            continue

        print_board() # Print board after the move

        if check_win(current_player_checker):
            winner = current_player_checker
            game_over = True
        elif check_draw():
            game_over = True
        else:
            switch_player()
            
    # Game end
    print_board() # Final board state
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

# --- Main execution ---
if __name__ == "__main__":
    play_game()
