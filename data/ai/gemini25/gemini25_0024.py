import os
import random
import sys

# --- GLOBAL CONSTANTS ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

# --- BOARD FUNCTIONS ---
def create_board():
    """
    Creates an empty Connect 4 board initialized with whitespaces.
    Returns:
        list: A 2D list representing the game board.
    """
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """
    Prints the current state of the Connect 4 board.
    Args:
        board (list): The game board to print.
    """
    os.system('clear')  # Clear screen for a cleaner display

    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    
    # Print board rows
    for r_idx in range(NUM_ROWS):
        print("+" + "---+" * NUM_COLS)
        row_content = []
        for c_idx in range(NUM_COLS):
            row_content.append(f" {board[r_idx][c_idx]} ")
        print("|" + "|".join(row_content) + "|")
    print("+" + "---+" * NUM_COLS)

# --- GAME LOGIC FUNCTIONS ---
def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.
    Args:
        player_checker (str): The checker symbol of the current player.
    Returns:
        int: The validated column index (0-indexed).
    """
    while True:
        try:
            col_input = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_input) != 1 or col_input not in COLUMN_LABELS:
                raise ValueError("Invalid column. Please enter a single letter from A to " + COLUMN_LABELS[-1] + ".")
            
            col_index = COLUMN_LABELS.index(col_input)
            return col_index
        except ValueError as e:
            print(f"Error: {e}")
        except EOFError:  # Handle Ctrl+D input gracefully
            print("\nGame ended by user. Goodbye!")
            sys.exit()

def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.
    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        player_checker (str): The checker symbol of the current player.
    Returns:
        int or None: The row index where the checker was placed, or None if the column is full.
    """
    for r_idx in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom to top
        if board[r_idx][col_index] == " ":
            board[r_idx][col_index] = player_checker
            return r_idx  # Return the row where the checker was placed
    return None  # Column is full

def check_win(board, player_checker, last_row, last_col):
    """
    Checks if the current player has won after their last move.
    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the current player.
        last_row (int): The row where the last checker was placed.
        last_col (int): The column where the last checker was placed.
    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Define directions for checking (horizontal, vertical, two diagonals)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal (top-left to bottom-right)
        (1, -1)   # Diagonal (top-right to bottom-left)
    ]

    for dr, dc in directions:
        count = 1  # Count of consecutive checkers, starting with the last placed one

        # Check in one direction
        for i in range(1, WIN_CONDITION):
            r, c = last_row + dr * i, last_col + dc * i
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
                count += 1
            else:
                break
        
        # Check in the opposite direction
        for i in range(1, WIN_CONDITION):
            r, c = last_row - dr * i, last_col - dc * i
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
                count += 1
            else:
                break
        
        if count >= WIN_CONDITION:
            return True
            
    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    Args:
        board (list): The game board.
    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # Board is full

# --- MAIN GAME FUNCTION ---
def play_connect4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board()
    
    # Randomly select the first player
    current_player_idx = random.randrange(NUM_PLAYERS)
    
    print_board(board)
    print(f"Player {CHECKERS[current_player_idx]} goes first!")

    game_over = False
    last_placed_row = -1
    last_placed_col = -1

    while not game_over:
        player_checker = CHECKERS[current_player_idx]
        
        valid_move_made = False
        while not valid_move_made:
            chosen_col_index = get_column_input(player_checker)
            
            last_placed_row = drop_checker(board, chosen_col_index, player_checker)
            last_placed_col = chosen_col_index

            if last_placed_row is not None:
                valid_move_made = True
            else:
                print(f"Error: Column {COLUMN_LABELS[chosen_col_index]} is full. Please choose another column.")
                # Player does not lose turn for a full column

        print_board(board)

        if check_win(board, player_checker, last_placed_row, last_placed_col):
            print(f"Player {player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

# --- ENTRY POINT ---
if __name__ == "__main__":
    play_connect4()
