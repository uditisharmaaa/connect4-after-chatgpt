import os
import random

# --- Global Constants (for easy modification) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Max 5 players
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    
    # Print column labels (A, B, C, ...)
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))

    # Print board content
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_display = "| "
        for c in range(len(board[0])):
            row_display += board[r][c] + " | "
        print(row_display)
    print("+---" * len(board[0]) + "+")

def get_column_from_input(prompt):
    """
    Prompts the user for a column input and validates it.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        str: The validated uppercase column letter.
    """
    while True:
        col_input = input(prompt).strip().upper()
        if len(col_input) == 1 and 'A' <= col_input <= chr(ord('A') + NUM_COLS - 1):
            return col_input
        else:
            print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + NUM_COLS - 1)}.")

def place_checker(board, col_char, player_checker):
    """
    Places a player's checker in the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_char (str): The uppercase letter representing the chosen column.
        player_checker (str): The checker symbol for the current player.

    Returns:
        tuple: (True, int) if checker was placed successfully, with the row index.
               (False, None) if the column is full.
    """
    col_index = ord(col_char) - ord('A')

    # Check if column is valid (already handled by get_column_from_input, but good for robustness)
    if not (0 <= col_index < NUM_COLS):
        return False, None

    # Find the lowest available row in the column
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True, r  # Return row index where checker was placed
    return False, None  # Column is full

def check_win(board, player_checker, last_row, last_col):
    """
    Checks if the given player has won the game after their last move.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol of the player to check.
        last_row (int): The row index of the last placed checker.
        last_col (int): The column index of the last placed checker.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[last_row][c] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][last_col] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check positive diagonal (bottom-left to top-right)
    # Start from the bottom-left of the potential diagonal and go up-right
    start_row = last_row + last_col - (NUM_COLS - 1) if last_row + last_col >= NUM_COLS else 0
    start_col = last_col - (last_row - start_row)
    
    count = 0
    r, c = start_row, start_col
    while r < NUM_ROWS and c < NUM_COLS and r >= 0 and c >= 0:
        if board[r][c] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        r += 1
        c += 1

    # Check negative diagonal (top-left to bottom-right)
    # Start from the top-left of the potential diagonal and go down-right
    start_row = last_row - min(last_row, last_col)
    start_col = last_col - min(last_row, last_col)
    
    count = 0
    r, c = start_row, start_col
    while r < NUM_ROWS and c < NUM_COLS:
        if board[r][c] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        r += 1
        c += 1

    return False

def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw

# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    last_placed_row = -1
    last_placed_col = -1

    while not game_over:
        current_checker = PLAYER_CHECKERS[current_player_index]
        
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        column_input = get_column_from_input(f"Player {current_checker}'s turn: ")
        
        placed_successfully, row_placed = place_checker(board, column_input, current_checker)
        
        if placed_successfully:
            last_placed_row = row_placed
            last_placed_col = ord(column_input) - ord('A')

            # Check for win
            if check_win(board, current_checker, last_placed_row, last_placed_col):
                print_board(board)
                print(f"Player {current_checker} won!")
                game_over = True
            # Check for draw if no win
            elif check_draw(board):
                print_board(board)
                print("It's a draw! The board is full.")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Column was full, inform player and don't switch turns
            print("That column is full. Please choose another column.")
            # The loop will re-prompt the current player

if __name__ == "__main__":
    play_connect_4()
