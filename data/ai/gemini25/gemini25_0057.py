import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    The board is a list of lists, initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    Columns are labeled with letters (A, B, C...).
    """
    clear_screen()

    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))

    # Print board rows
    for row in board:
        print("+---+---+---+---+---+---+---+") # This assumes 7 columns, adjust for general N_COLS
        row_str = "|"
        for cell in row:
            row_str += f" {cell} |"
        print(row_str)
    print("+---+---+---+---+---+---+---+") # This assumes 7 columns, adjust for general N_COLS

def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(user_input) - ord('A')

            if 0 <= col_index < NUM_COLS:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
        except Exception:
            print("Invalid input. Please try again.")

def drop_checker(board, col_index, checker):
    """
    Drops the checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for row_index in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True, row_index, col_index
    return False, -1, -1 # Column is full

def check_win(board, checker, last_row, last_col):
    """
    Checks if the current player has won after placing a checker at (last_row, last_col).
    Checks horizontally, vertically, and both diagonals.
    """
    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[last_row][c] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][last_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check positive diagonal (bottom-left to top-right)
    count = 0
    # Calculate start of this diagonal
    start_row = last_row - min(last_row, last_col)
    start_col = last_col - min(last_row, last_col)
    while start_row < NUM_ROWS and start_col < NUM_COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1

    # Check negative diagonal (top-left to bottom-right)
    count = 0
    # Calculate start of this diagonal
    start_row = last_row - min(last_row, NUM_COLS - 1 - last_col)
    start_col = last_col + min(last_row, NUM_COLS - 1 - last_col)
    while start_row < NUM_ROWS and start_col >= 0:
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
    Checks if the board is completely full, indicating a draw.
    """
    for row in board:
        if " " in row:
            return False  # There's still an empty space
    return True # Board is full

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    player_index = random.randint(0, NUM_PLAYERS - 1) # Randomly choose first player
    game_over = False
    
    while not game_over:
        current_player_checker = CHECKERS[player_index]
        print_board(board)

        col_index = get_column_input(current_player_checker)
        
        # Keep asking for input until a valid move is made
        move_successful = False
        while not move_successful:
            successful_drop, last_row, last_col = drop_checker(board, col_index, current_player_checker)
            if successful_drop:
                move_successful = True
            else:
                print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
                col_index = get_column_input(current_player_checker) # Ask for new input

        if check_win(board, current_player_checker, last_row, last_col):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            player_index = (player_index + 1) % NUM_PLAYERS # Switch to next player

if __name__ == "__main__":
    play_game()
