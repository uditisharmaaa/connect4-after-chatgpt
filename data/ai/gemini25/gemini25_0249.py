import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
# Get only the checkers for the number of players specified
ACTIVE_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]

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
        board.append([' '] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    Includes column labels (A, B, C, ...) and the board grid.
    """
    clear_screen()

    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(NUM_COLS)]
    print('  ' + '   '.join(col_labels))

    # Print top border
    print('+' + '---+'.join(['-'] * NUM_COLS) + '+')

    # Print rows
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---+'.join(['-'] * NUM_COLS) + '+')

def get_column_from_input(prompt):
    """
    Gets a column letter from the user and validates it.
    Returns the 0-indexed column number if valid, otherwise None.
    """
    while True:
        user_input = input(prompt).strip().upper()

        if len(user_input) != 1 or not ('A' <= user_input[0] < chr(ord('A') + NUM_COLS)):
            print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + NUM_COLS - 1)}.")
            continue

        col_index = ord(user_input[0]) - ord('A')
        return col_index

def place_checker(board, col, checker):
    """
    Places a checker in the specified column.
    Returns True if the checker was placed successfully, False if the column is full.
    """
    # Iterate from the bottom row upwards
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False # Column is full

def check_win(board, checker):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
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
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False # Found an empty spot, not a draw yet
    return True # Board is full

# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = ACTIVE_CHECKERS[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        chosen_col = None
        valid_move = False
        while not valid_move:
            col_index = get_column_from_input(f"Player {current_checker}, please enter a column: ")
            
            # Check if the column is full
            if col_index is not None and board[0][col_index] != ' ': # Check the top row of the chosen column
                print("Column is full. Please choose another column.")
                continue

            if col_index is not None:
                # Attempt to place the checker
                if place_checker(board, col_index, current_checker):
                    valid_move = True
                else:
                    # This case should ideally not be reached if board[0][col_index] check is correct
                    # but kept for robustness.
                    print("Could not place checker. Column might be full (internal error).")
            # If col_index is None, get_column_from_input already printed an error and will loop.


        # After a valid move is made
        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_checker = ACTIVE_CHECKERS[current_player_index]

    print("\n--- Game Over ---")

if __name__ == "__main__":
    main()
