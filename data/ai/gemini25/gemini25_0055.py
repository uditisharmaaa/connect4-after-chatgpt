import os
import random
import sys

# --- GLOBAL CONSTANTS ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for A-Z column labels
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers for players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Number of checkers in a row to win
WIN_CONDITION = 4

# --- HELPER FUNCTIONS ---

def clear_screen():
    """Clears the terminal screen."""
    # for windows
    if os.name == 'nt':
        os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board,
              initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for i in range(NUM_COLS):
        print(f"  {chr(ord('A') + i)} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

    # Print rows
    for r in range(NUM_ROWS):
        print("|", end="")
        for c in range(NUM_COLS):
            print(f" {board[r][c]} |", end="")
        print()

        # Print row separator
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()

def get_player_input(player_checker, board):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.
        board (list): The 2D list representing the game board.

    Returns:
        int: The 0-indexed column number if the input is valid.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B).")
                continue

            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column. Please choose a column between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            if board[0][col_index] != " ":  # Check if the top row of the column is full
                print("Column is full. Please choose another column.")
                continue

            return col_index

        except EOFError:
            print("\nExiting game.")
            sys.exit()
        except Exception:
            print("An unexpected error occurred. Please try again.")

def place_checker(board, col_index, player_checker):
    """
    Places the player's checker in the lowest available space of the given column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column number.
        player_checker (str): The checker symbol of the current player.

    Returns:
        tuple: A tuple (row, col) indicating where the checker was placed,
               or None if the column is full (though this should be caught by validation).
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return (r, col_index)
    return None # Should not be reached if validation is correct

def check_win(board, last_row, last_col, player_checker):
    """
    Checks if the player who just placed a checker at (last_row, last_col) has won.

    Args:
        board (list): The 2D list representing the game board.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[last_row][c] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][last_col] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    # Find the starting point (top-leftmost cell of this diagonal)
    start_row = last_row - min(last_row, last_col)
    start_col = last_col - min(last_row, last_col)
    while start_row < NUM_ROWS and start_col < NUM_COLS:
        if board[start_row][start_col] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1

    # Check diagonal (top-right to bottom-left)
    count = 0
    # Find the starting point (top-rightmost cell of this diagonal)
    start_row = last_row - min(last_row, NUM_COLS - 1 - last_col)
    start_col = last_col + min(last_row, NUM_COLS - 1 - last_col)
    while start_row < NUM_ROWS and start_col >= 0:
        if board[start_row][start_col] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        start_row += 1
        start_col -= 1

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw

# --- MAIN GAME LOGIC ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        col_index = get_player_input(player_checker, board)
        
        last_placement = place_checker(board, col_index, player_checker)
        
        # This assert should technically not be hit if get_player_input works correctly
        assert last_placement is not None, "Failed to place checker, column might be full despite validation."
        
        last_row, last_col = last_placement

        if check_win(board, last_row, last_col, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("Thanks for playing!")

if __name__ == "__main__":
    main()
