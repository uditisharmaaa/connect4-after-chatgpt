import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
EMPTY_CELL = " "

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates a new game board initialized with empty cells.
    """
    board = []
    for _ in range(rows):
        board.append([EMPTY_CELL] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    """
    os.system('clear')  # Clear the screen

    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f" {string.ascii_uppercase[col_index]} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()

def get_column_input(prompt_message, num_cols):
    """
    Gets and validates column input from the player.
    Returns the 0-indexed column number if valid, otherwise continually prompts.
    """
    while True:
        user_input = input(prompt_message).upper()
        if len(user_input) == 1 and 'A' <= user_input <= string.ascii_uppercase[num_cols - 1]:
            col_index = ord(user_input) - ord('A')
            return col_index
        else:
            print(f"Invalid input. Please enter a single letter from A to {string.ascii_uppercase[num_cols - 1]}.")

def drop_checker(board, col_index, checker):
    """
    Places the checker in the lowest available space in the specified column.
    Returns True if successful, False if the column is full.
    """
    for row_index in range(len(board) - 1, -1, -1):  # Start from the bottom row
        if board[row_index][col_index] == EMPTY_CELL:
            board[row_index][col_index] = checker
            return True
    return False # Column is full

# --- Win Condition Checks ---

def check_horizontal_win(board, checker, win_condition):
    """
    Checks for a horizontal win for the given checker.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == checker for i in range(win_condition)):
                return True
    return False

def check_vertical_win(board, checker, win_condition):
    """
    Checks for a vertical win for the given checker.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == checker for i in range(win_condition)):
                return True
    return False

def check_diagonal_win(board, checker, win_condition):
    """
    Checks for diagonal wins (both directions) for the given checker.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check positive slope diagonals (bottom-left to top-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == checker for i in range(win_condition)):
                return True

    # Check negative slope diagonals (top-left to bottom-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == checker for i in range(win_condition)):
                return True
    return False

def check_win(board, checker, win_condition):
    """
    Checks if the given checker has won the game.
    """
    return (check_horizontal_win(board, checker, win_condition) or
            check_vertical_win(board, checker, win_condition) or
            check_diagonal_win(board, checker, win_condition))

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.
    """
    for row in board:
        if EMPTY_CELL in row:
            return False
    return True

# --- Game Logic ---

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    while not game_over:
        print_board(board)
        
        current_checker = PLAYER_CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")

        col_input = get_column_input(f"Player {current_checker}, your turn: ", NUM_COLS)

        if drop_checker(board, col_input, current_checker):
            # Checker was successfully dropped
            if check_win(board, current_checker, WIN_CONDITION):
                game_over = True
                winner_checker = current_checker
            elif check_draw(board):
                game_over = True
            else:
                # Move to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {string.ascii_uppercase[col_input]} is full. Please choose another column.")
            # The player does not lose their turn if the column is full.
            # They will be prompted again in the next iteration of the loop.

    print_board(board) # Print final board
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    main()
