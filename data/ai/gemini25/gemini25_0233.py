import os
import random

# --- Constants (Global Variables) ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Functions ---

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
    Clears the screen and prints the current state of the board.
    Columns are labeled A, B, C, etc.
    """
    os.system('clear')  # Clear the screen

    # Print column labels
    column_labels = [chr(ord('A') + i) for i in range(NUM_COLS)]
    print("  " + "   ".join(column_labels))

    # Print board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(user_input) != 1 or not 'A' <= user_input <= chr(ord('A') + NUM_COLS - 1):
                print(f"Invalid input. Please enter a single letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue
            
            col_index = ord(user_input) - ord('A')
            return col_index
        except Exception:
            print("Invalid input. Please try again.")

def place_checker(board, col_index, current_player_checker):
    """
    Places the current player's checker in the lowest available space in the given column.
    Returns True if the checker was placed successfully, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col_index] == " ":
            board[r][col_index] = current_player_checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """
    Checks if the given checker has formed a winning line (4 in a row)
    horizontally, vertically, or diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # There's still an empty space
    return True  # Board is full

# --- Main Game Logic ---

def play_game():
    """
    Manages the main game loop for Connect 4.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        
        valid_turn = False
        while not valid_turn:
            col_index = get_column_input(current_player_checker)
            
            if place_checker(board, col_index, current_player_checker):
                valid_turn = True
            else:
                print("Column is full. Please choose another column.")
                # Player does not lose turn, will be prompted again

        print_board(board) # Print board after checker is placed

        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# --- Start the game ---
if __name__ == "__main__":
    play_game()
