import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS] # Limit to max 5 checkers
WIN_CONDITION = 4 # Number of checkers in a row to win

# --- Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the current state of the board.
    """
    clear_screen()
    cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:cols]))
    
    for r_idx, row in enumerate(board):
        # Print top border of the row
        print("+" + "---+".join(["" for _ in range(cols)]) + "---+")
        
        # Print row content
        row_str = "|"
        for cell in row:
            row_str += f" {cell} |"
        print(row_str)
    
    # Print bottom border of the last row
    print("+" + "---+".join(["" for _ in range(cols)]) + "---+")


def get_column_input(current_player_checker, board):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        board (list): The current state of the board.

    Returns:
        int: The 0-indexed column number if the input is valid.
    """
    cols = len(board[0])
    valid_columns = string.ascii_uppercase[:cols]
    
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            
            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue
            
            if col_char not in valid_columns:
                print(f"Invalid column. Please choose a column from {valid_columns[0]} to {valid_columns[-1]}.")
                continue
            
            col_index = ord(col_char) - ord('A')
            
            # Check if the column is full
            if board[0][col_index] != " ":
                print(f"Column {col_char} is full. Please choose another column.")
                continue
            
            return col_index
        except Exception:
            print("An unexpected error occurred. Please try again.")

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The current state of the board.
        col_index (int): The 0-indexed column number to drop the checker into.
        checker (str): The checker symbol to place.

    Returns:
        tuple: A tuple (row_index, col_index) where the checker was placed,
               or None if the column is full (though this should be caught by validation).
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1): # Iterate from bottom to top
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r, col_index
    return None # Column is full

def check_win(board, row, col, checker):
    """
    Checks if the given player has won the game after placing a checker at (row, col).

    Args:
        board (list): The current state of the board.
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(cols):
        if board[row][c] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(rows):
        if board[r][col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    # Start from the 'start' of the diagonal (row - min_offset, col - min_offset)
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    while start_row < rows and start_col < cols:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1

    # Check diagonal (top-right to bottom-left)
    count = 0
    # Start from the 'start' of the diagonal (row - min_offset, col + min_offset)
    start_row = row - min(row, cols - 1 - col)
    start_col = col + min(row, cols - 1 - col)
    while start_row < rows and start_col >= 0:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        start_row += 1
        start_col -= 1

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The current state of the board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    cols = len(board[0])
    for c in range(cols):
        if board[0][c] == " ": # If the top row of any column has a space, board is not full
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Determine initial player and player order
    player_indices = list(range(NUM_PLAYERS))
    random.shuffle(player_indices) # Randomize the starting order
    
    current_player_index = player_indices[0]
    
    game_over = False
    
    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        print_board(board)
        
        col_index = get_column_input(current_player_checker, board)
        
        placed_pos = drop_checker(board, col_index, current_player_checker)
        
        if placed_pos: # Checker was successfully placed
            row_placed, col_placed = placed_pos
            
            if check_win(board, row_placed, col_placed, current_player_checker):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("It's a draw! The board is full.")
                game_over = True
            else:
                # Move to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        # else:
        #     # This case should ideally not be reached if get_column_input is robust,
        #     # as it should re-prompt for full columns.
        #     # If it somehow does, the current player does not lose their turn due to invalid input.
        #     # The prompt loop in get_column_input handles this.
        #     pass 

    print("Game Over!")

if __name__ == "__main__":
    main()
