import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns supported by current labeling
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
# Ensure we have enough checkers for the number of players
assert 2 <= NUM_PLAYERS <= len(PLAYER_CHECKERS), "NUM_PLAYERS must be between 2 and 5."

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    The board is a list of lists, initialized with whitespaces.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board with column labels.
    Example:
      A   B   C   D   E   F   G
    +---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |
    ...
    """
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    sys.stdout.write('  ')
    for i in range(num_cols):
        sys.stdout.write(f'{chr(ord("A") + i)}   ')
    sys.stdout.write('\n')

    # Print board content
    for r in range(len(board)):
        # Top border for each row
        sys.stdout.write('+')
        for _ in range(num_cols):
            sys.stdout.write('---+')
        sys.stdout.write('\n')

        # Row content
        sys.stdout.write('|')
        for c in range(num_cols):
            sys.stdout.write(f' {board[r][c]} |')
        sys.stdout.write('\n')

    # Bottom border for the last row
    sys.stdout.write('+')
    for _ in range(num_cols):
        sys.stdout.write('---+')
    sys.stdout.write('\n')

def get_column_from_input(prompt, num_cols):
    """
    Prompts the player for a column input and validates it.
    Returns the 0-indexed column number if valid.
    """
    while True:
        try:
            col_input = input(prompt).strip().upper()
            if not col_input:
                raise ValueError("Input cannot be empty.")
            
            col_index = ord(col_input) - ord('A')

            if not (0 <= col_index < num_cols):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
            else:
                return col_index
        except TypeError: # This handles cases where input is not a single character, e.g. "AA" or "1"
            print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C).")
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a single uppercase letter (e.g., A, B, C).")

def place_checker(board, col, checker):
    """
    Places the checker in the lowest available row of the given column.
    Returns True if successful, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col] == ' ':
            board[r][col] = checker
            return True
    return False # Column is full

def check_win(board, checker, win_length):
    """
    Checks if the given checker has formed a win_length sequence
    horizontally, vertically, or diagonally.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_length + 1):
            if all(board[r][c + i] == checker for i in range(win_length)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - win_length + 1):
            if all(board[r + i][c] == checker for i in range(win_length)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - win_length + 1):
        for c in range(num_cols - win_length + 1):
            if all(board[r + i][c + i] == checker for i in range(win_length)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(num_rows - win_length + 1):
        for c in range(win_length - 1, num_cols):
            if all(board[r + i][c - i] == checker for i in range(win_length)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled (draw).
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw
    return True  # Board is full

# --- Main Game Logic ---

def play_connect4():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print("Welcome to Connect 4!\n")
    print_board(board)
    print(f"Players: {', '.join(players)}")
    print(f"Player {players[current_player_index]} goes first!\n")

    game_over = False
    winner = None

    while not game_over:
        current_checker = players[current_player_index]
        
        while True:
            col_index = get_column_from_input(f"Player {current_checker}, please enter a column: ", NUM_COLS)
            
            if place_checker(board, col_index, current_checker):
                break  # Checker placed successfully, exit inner loop
            else:
                print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
                # Player does not lose turn for choosing a full column

        clear_screen()
        print_board(board)

        if check_win(board, current_checker, WIN_SEQUENCE_LENGTH):
            winner = current_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game End
    if winner:
        print(f"\nPlayer {winner} won!")
    else:
        print("\nIt's a draw!")
    
    print("Thank you for playing!")

if __name__ == "__main__":
    play_connect4()
