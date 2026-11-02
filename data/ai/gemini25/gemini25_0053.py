import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Global Variables ---
board = []
players = []

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Initializes the game board with empty spaces."""
    global board
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(NUM_COLS)]))
    
    # Print board content
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
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not (len(col_char) == 1 and 'A' <= col_char <= chr(ord('A') + NUM_COLS - 1)):
                raise ValueError("Invalid column. Please enter a letter from A to " + chr(ord('A') + NUM_COLS - 1))
            
            col = ord(col_char) - ord('A')
            
            if board[0][col] != " ": # Check if the top of the column is full
                raise ValueError("Column is full. Please choose another column.")

            return col
        except ValueError as e:
            print(f"Error: {e}")
        except Exception:
            print("An unexpected error occurred. Please try again.")

def place_checker(col, checker):
    """
    Places the checker in the lowest available space in the specified column.
    Returns True if successful, False if the column is full (should not happen with prior validation).
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False # Column is full

def check_win(checker):
    """
    Checks if the current player (with 'checker') has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c+i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
            if all(board[r+i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r-i][c+i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw():
    """Checks if the board is full, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True

def setup_players():
    """Initializes the player list with checkers."""
    global players
    players = CHECKERS[:NUM_PLAYERS]

def main():
    """Main function to run the Connect 4 game."""
    create_board()
    setup_players()

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner = None

    while not game_over:
        print_board()
        current_player_checker = players[current_player_index]

        col = get_column_input(current_player_checker)
        
        place_checker(col, current_player_checker)

        if check_win(current_player_checker):
            winner = current_player_checker
            game_over = True
        elif check_draw():
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print_board()
    if winner:
        print(f"Player {winner} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    main()
