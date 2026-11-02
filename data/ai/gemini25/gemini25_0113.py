import os
import random
import string

# --- Constants (Can be changed for different game setups) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Between 2 and 5
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Clears the screen and prints the current state of the Connect 4 board.
    """
    os.system('clear')  # Clear the console for a clean display

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:NUM_COLS]))

    # Print top border
    print("+" + "---+" * NUM_COLS)

    # Print rows with checkers
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * NUM_COLS)

def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_input) != 1 or col_input not in string.ascii_uppercase[:NUM_COLS]:
                print(f"Invalid input. Please enter a single letter from A to {string.ascii_uppercase[NUM_COLS-1]}.")
                continue
            
            col_index = ord(col_input) - ord('A')
            return col_index
        except Exception:
            print("Invalid input. Please try again.")

def drop_checker(board, col_index, checker):
    """
    Drops the checker into the lowest available space in the specified column.
    Returns True if the checker was placed successfully, False if the column is full.
    """
    # Iterate from the bottom row upwards
    for row_index in range(NUM_ROWS - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True
    return False # Column is full

def check_win(board, checker):
    """
    Checks if the current player has won the game.
    Returns True if a win condition is met, False otherwise.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
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
    Checks if the board is completely filled (a draw).
    Returns True if it's a draw, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # Board is full

# --- Main Game Logic ---

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        valid_turn = False
        while not valid_turn:
            col_index = get_column_input(current_player_checker)

            if drop_checker(board, col_index, current_player_checker):
                valid_turn = True
            else:
                print(f"Column {string.ascii_uppercase[col_index]} is full. Please choose another column.")
                # Player does NOT lose their turn for a full column

        # After dropping the checker, check for win or draw
        if check_win(board, current_player_checker):
            winner_checker = current_player_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        
        # Switch to the next player
        if not game_over: # Only switch player if the game isn't over yet
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game over, print final board and result
    print_board(board)
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    main()
