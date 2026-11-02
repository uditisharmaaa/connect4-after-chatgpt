import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4

# Checkers available
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

# --- Board Functions ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board with column labels.
    Clears the screen before printing.
    """
    os.system('clear')

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print board content
    for r in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(len(board[0])):
            print(f" {board[r][c]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

def get_column_index(col_char, num_cols):
    """
    Converts a column character (e.g., 'A') to a 0-based index.
    Returns -1 for invalid characters.
    """
    if not isinstance(col_char, str) or len(col_char) != 1:
        return -1
    
    col_char = col_char.upper()
    col_index = ord(col_char) - ord('A')
    
    if 0 <= col_index < num_cols:
        return col_index
    else:
        return -1

def is_valid_move(board, col_index):
    """
    Checks if a move to the given column is valid (column exists and is not full).
    """
    if not (0 <= col_index < len(board[0])):
        return False
    
    # Check if the top row of the column is empty
    return board[0][col_index] == " "

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.
    Assumes the move is valid.
    Returns the row index where the checker landed.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r
    return -1 # Should not happen if is_valid_move is called first

# --- Win Condition Functions ---
def check_win(board, checker):
    """
    Checks if the given checker has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found

# --- Main Game Logic ---
def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = PLAYER_CHECKERS[current_player_index]

    game_over = False
    
    while not game_over:
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        # Get valid player input
        while True:
            col_input = input().strip()
            col_index = get_column_index(col_input, NUM_COLS)

            if col_index == -1:
                print("Invalid column. Please enter a letter from A to", chr(ord('A') + NUM_COLS - 1) + ":")
            elif not is_valid_move(board, col_index):
                print(f"Column {col_input.upper()} is full. Please choose another column:")
            else:
                break # Valid input, break out of the input loop

        # Place the checker
        drop_checker(board, col_index, current_checker)

        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_checker = PLAYER_CHECKERS[current_player_index]

if __name__ == "__main__":
    play_game()
