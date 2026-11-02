import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# --- Functions ---

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
    Clears the screen and prints the current state of the board.
    """
    os.system('clear')  # Clear the terminal screen

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(len(board[0])):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print board rows
    for row_idx in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()
        print("|", end="")
        for col_idx in range(len(board[0])):
            print(f" {board[row_idx][col_idx]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()


def get_player_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column choice and validates the input.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        except TypeError:
            print("Invalid input. Please enter a letter.")
        except Exception:
            print("An unexpected error occurred. Please try again.")


def place_checker(board, col_index, current_player_checker):
    """
    Places the current player's checker in the lowest available space
    of the specified column. Returns True if successful, False if the
    column is full.
    """
    for row_idx in range(len(board) - 1, -1, -1):  # Iterate from bottom to top
        if board[row_idx][col_index] == " ":
            board[row_idx][col_index] = current_player_checker
            return True
    return False  # Column is full


def check_win(board, player_checker, win_length):
    """
    Checks if the given player has achieved 'win_length' checkers in a row
    (horizontally, vertically, or diagonally).
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_length + 1):
            if all(board[r][c + i] == player_checker for i in range(win_length)):
                return True

    # Check vertical
    for r in range(num_rows - win_length + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == player_checker for i in range(win_length)):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(win_length - 1, num_rows):
        for c in range(num_cols - win_length + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_length)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(num_rows - win_length + 1):
        for c in range(num_cols - win_length + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_length)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for row in board:
        if " " in row:
            return False  # There is at least one empty space
    return True  # Board is full


def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    print_board(board)
    print(f"Player {players[current_player_index]} starts the game!")

    while not game_over:
        current_player_checker = players[current_player_index]
        
        col_index = get_player_input(current_player_checker, NUM_COLS)
        
        if place_checker(board, col_index, current_player_checker):
            print_board(board)

            if check_win(board, current_player_checker, WIN_LENGTH):
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print("The board is full. It's a draw!")
                game_over = True
            else:
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # Player does not lose turn if column is full, they re-enter input

if __name__ == "__main__":
    main()
