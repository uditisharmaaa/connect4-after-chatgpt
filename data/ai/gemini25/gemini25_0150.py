import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels
NUM_PLAYERS = 2  # Between 2 and 5 players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(NUM_COLS):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print the board with separators
    for row in board:
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

def get_column_index(column_char):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding integer index.

    Args:
        column_char (str): The uppercase character representing the column.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if len(column_char) == 1 and 'A' <= column_char <= chr(ord('A') + NUM_COLS - 1):
        return ord(column_char) - ord('A')
    return -1

def is_valid_input(column_char):
    """
    Checks if the player's column input is valid.

    Args:
        column_char (str): The character input by the player.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    col_index = get_column_index(column_char)
    return col_index != -1

def get_next_available_row(board, col_index):
    """
    Finds the lowest available row in a given column.

    Args:
        board (list): The game board.
        col_index (int): The index of the column.

    Returns:
        int: The row index where the checker can be placed, or -1 if the column is full.
    """
    for row_index in range(NUM_ROWS - 1, -1, -1):
        if board[row_index][col_index] == " ":
            return row_index
    return -1 # Column is full

def place_checker(board, col_index, player_checker):
    """
    Places a checker in the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was placed successfully, False if the column was full.
    """
    row_index = get_next_available_row(board, col_index)
    if row_index != -1:
        board[row_index][col_index] = player_checker
        return True
    return False

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal wins
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r][c + i] == player_checker for i in range(4)):
                return True

    # Check vertical wins
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == player_checker for i in range(4)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS - 3):
            if all(board[r + i][c + i] == player_checker for i in range(4)):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for r in range(3, NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r - i][c + i] == player_checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True # Board is full

# --- Main Game Logic ---

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner = None

    while not game_over:
        player_checker = CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {player_checker}, please enter a column: ", end="")

        while True:
            column_input = input().strip().upper()
            
            if not is_valid_input(column_input):
                print("Invalid column. Please enter a letter from A to", chr(ord('A') + NUM_COLS - 1) + ": ", end="")
                continue
            
            col_index = get_column_index(column_input)
            
            if not place_checker(board, col_index, player_checker):
                print(f"Column {column_input} is full. Please choose another column: ", end="")
                continue
            
            break # Valid move made, exit inner loop

        if check_win(board, player_checker):
            print_board(board)
            winner = player_checker
            game_over = True
        elif check_draw(board):
            print_board(board)
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game End
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

# Run the game
if __name__ == "__main__":
    main()
