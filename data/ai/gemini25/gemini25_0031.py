import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    print("  " + "   ".join(COLUMN_LABELS[:NUM_COLS]))
    for r in range(len(board)):
        print("+" + "---+".join(["" for _ in range(NUM_COLS + 1)]))
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+" + "---+".join(["" for _ in range(NUM_COLS + 1)]))

def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.

    Returns:
        int: The validated column index (0-based).
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1:
                raise ValueError("Invalid input. Please enter a single letter (e.g., A).")
            
            col_index = ord(col_char) - ord('A')
            
            if not (0 <= col_index < NUM_COLS):
                raise ValueError("Column out of board range. Please choose a valid column.")
            
            return col_index
        except ValueError as e:
            print(f"Error: {e}")

def place_checker(board, col_index, player_checker):
    """
    Places the player's checker in the lowest available space of the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to place the checker.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False # Column is full

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Logic ---

def play_game():
    """Manages the main Connect 4 game flow."""
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        valid_turn = False
        while not valid_turn:
            col_input_index = get_column_input(player_checker)
            
            if place_checker(board, col_input_index, player_checker):
                valid_turn = True
            else:
                print(f"Column {COLUMN_LABELS[col_input_index]} is full. Please choose another column.")
                # Player does NOT lose turn on full column, they retry input

        print_board(board) # Print board after valid move

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
