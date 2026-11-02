import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns for letter labels
NUM_PLAYERS = 2  # Between 2 and 5 players

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
EMPTY_CELL = " "

# --- Board Functions ---

def create_board(rows, cols):
    """Creates an empty Connect 4 board."""
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board to the console."""
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(len(board[0]))]))
    
    # Print board rows
    for r in range(len(board)):
        print("+" + "---+".join(["" for _ in range(len(board[0]))]) + "+")
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+" + "---+".join(["" for _ in range(len(board[0]))]) + "+")

def get_column_input(player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").upper()
        
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter (e.g., A, B).")
            continue

        col_char_code = ord(col_input)
        col_index = col_char_code - ord('A')

        if not (0 <= col_index < num_cols):
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
            continue
        
        return col_index

def place_checker(board, col_index, player_checker):
    """
    Places the player's checker in the specified column.
    Returns True if successful, False if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == EMPTY_CELL:
            board[r][col_index] = player_checker
            return True
    return False # Column is full

# --- Win Condition Functions ---

def check_win(board, player_checker):
    """Checks if the current player has won the game."""
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == player_checker for i in range(4)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == player_checker for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == player_checker for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == player_checker for i in range(4)):
                return True
                
    return False

def check_draw(board):
    """Checks if the board is full (a draw)."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == EMPTY_CELL:
                return False
    return True

# --- Main Game Loop ---

def play_connect4():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner = None

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        valid_turn = False
        while not valid_turn:
            col_index = get_column_input(current_player_checker, NUM_COLS)
            if place_checker(board, col_index, current_player_checker):
                valid_turn = True
            else:
                print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
                # Player does not lose turn for a full column

        if check_win(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            winner = current_player_checker
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        
        # Switch to the next player
        if not game_over: # Only switch if the game isn't over yet
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_connect4()
