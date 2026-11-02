import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Board Initialization ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    """
    return [[" "] * cols for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    """
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(len(board[0])):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

    # Print board rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        # Print row separator
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()

# --- Game Logic ---
def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
            if not user_input:
                print("Input cannot be empty. Please enter a column letter (e.g., A).")
                continue

            col_char = user_input[0]
            if not ('A' <= col_char <= chr(ord('A') + num_cols - 1)):
                print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + num_cols - 1)}.")
                continue

            col_idx = ord(col_char) - ord('A')
            return col_idx
        except IndexError:
            print("Invalid input format. Please enter a single column letter (e.g., A).")
        except Exception:
            print("An unexpected error occurred. Please try again.")


def drop_checker(board, col_idx, checker):
    """
    Drops the checker into the specified column.
    Returns True if the checker was placed, False if the column is full.
    """
    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return True
    return False # Column is full

def check_win(board, checker, win_condition):
    """
    Checks if the current player has won the game.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_condition + 1):
            if all(board[r][c + i] == checker for i in range(win_condition)):
                return True

    # Check vertical
    for r in range(rows - win_condition + 1):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(win_condition)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - win_condition + 1):
        for c in range(cols - win_condition + 1):
            if all(board[r + i][c + i] == checker for i in range(win_condition)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_condition - 1, rows):
        for c in range(cols - win_condition + 1):
            if all(board[r - i][c + i] == checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.
    """
    for row in board:
        if " " in row:
            return False
    return True # Board is full

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_idx]
        print_board(board)
        
        valid_turn = False
        while not valid_turn:
            col_idx = get_column_input(current_player_checker, NUM_COLS)
            
            if drop_checker(board, col_idx, current_player_checker):
                valid_turn = True
            else:
                print(f"Column {chr(ord('A') + col_idx)} is full. Please choose another column.")
                # The turn is not lost, player is prompted again for a valid move

        print_board(board) # Print board after valid move

        if check_win(board, current_player_checker, WIN_CONDITION):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
