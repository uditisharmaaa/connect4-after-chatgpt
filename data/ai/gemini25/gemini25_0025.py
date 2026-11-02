import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
BOARD_EMPTY_CELL = " "

# --- Board Functions ---

def create_board(rows, cols):
    """Creates an empty Connect 4 board."""
    board = []
    for _ in range(rows):
        board.append([BOARD_EMPTY_CELL] * cols)
    return board

def print_board(board):
    """Prints the Connect 4 board to the console."""
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print board content
    for row in board:
        print("+", end="")
        for _ in row:
            print("---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in board[0]:
        print("---+", end="")
    print()

def get_column_letter(col_index):
    """Converts a column index to its corresponding letter (e.g., 0 -> 'A')."""
    return chr(ord('A') + col_index)

def get_column_index(col_letter):
    """Converts a column letter to its corresponding index (e.g., 'A' -> 0)."""
    return ord(col_letter.upper()) - ord('A')

def is_valid_column_input(col_input, num_cols):
    """
    Checks if the user's column input is valid.
    A valid input is a single uppercase letter within the board's range.
    """
    if len(col_input) != 1:
        return False
    
    col_letter = col_input.upper()
    if not ('A' <= col_letter <= chr(ord('A') + num_cols - 1)):
        return False
    
    return True

def find_lowest_empty_row(board, col_index):
    """
    Finds the lowest empty row in a given column.
    Returns the row index if an empty space is found, otherwise -1.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == BOARD_EMPTY_CELL:
            return r
    return -1

def place_checker(board, player_checker, col_index):
    """
    Places the player's checker in the specified column.
    Returns True if the checker was placed successfully, False if the column is full.
    """
    row_to_place = find_lowest_empty_row(board, col_index)
    if row_to_place != -1:
        board[row_to_place][col_index] = player_checker
        return True
    return False

# --- Win Condition Functions ---

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.
    Checks for horizontal, vertical, and diagonal wins.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal win
    for r in range(rows):
        for c in range(cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical win
    for c in range(cols):
        for r in range(rows - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal win (positive slope)
    for r in range(rows - WIN_SEQUENCE_LENGTH + 1):
        for c in range(cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal win (negative slope)
    for r in range(WIN_SEQUENCE_LENGTH - 1, rows):
        for c in range(cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True
    
    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == BOARD_EMPTY_CELL:
                return False
    return True

# --- Game Logic ---

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Get checkers for the number of players
    active_player_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = active_player_checkers[current_player_index]
        
        print_board(board)
        print(f"Player {current_player_checker}, please enter a column: ", end="")

        column_input = input()

        if not is_valid_column_input(column_input, NUM_COLS):
            print("Invalid input. Please enter a valid column letter (e.g., 'A').")
            continue # Player does not lose turn

        col_index = get_column_index(column_input)

        if not place_checker(board, current_player_checker, col_index):
            print("Column is full! Please choose another column.")
            continue # Player does not lose turn
        
        # Check for win
        if check_win(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw! The board is full.")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    main()
