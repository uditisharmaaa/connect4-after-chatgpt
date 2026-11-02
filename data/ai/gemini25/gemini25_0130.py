import os
import random
import sys

# --- Global Constants ---
# Board dimensions (can be changed, max 26 columns)
NUM_ROWS = 6
NUM_COLS = 7

# Number of players (between 2 and 5)
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Number of checkers in a row to win
CONNECT_N = 4

# --- Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with spaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
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
    # Clear the screen before printing the updated board
    os.system('clear')

    # Print column labels (A, B, C, ...)
    sys.stdout.write("  ")
    for col_idx in range(len(board[0])):
        sys.stdout.write(f"{chr(ord('A') + col_idx)}   ")
    sys.stdout.write("\n")

    # Print the board with separators
    for row_idx in range(len(board)):
        sys.stdout.write("+")
        for _ in range(len(board[0])):
            sys.stdout.write("---+")
        sys.stdout.write("\n")

        sys.stdout.write("|")
        for col_idx in range(len(board[0])):
            sys.stdout.write(f" {board[row_idx][col_idx]} |")
        sys.stdout.write("\n")

    # Print the bottom separator
    sys.stdout.write("+")
    for _ in range(len(board[0])):
        sys.stdout.write("---+")
    sys.stdout.write("\n")

def get_player_input(player_checker, num_cols):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column chosen by the player.
    """
    while True:
        try:
            column_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()

            # Check if input is a single uppercase letter
            if len(column_input) != 1 or not ('A' <= column_input[0] <= chr(ord('A') + num_cols - 1)):
                print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
                continue

            col_index = ord(column_input[0]) - ord('A')
            return col_index
        except Exception:
            # Catch any unexpected errors, though the specific checks above handle most cases
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")

def drop_checker(board, col_index, player_checker):
    """
    Places the player's checker into the specified column.
    The checker falls to the lowest available space.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        player_checker (str): The checker symbol of the current player.

    Returns:
        tuple: (bool, int) - True if the checker was successfully placed, False otherwise.
               The second element is the row index where the checker landed, or -1 if failed.
    """
    num_rows = len(board)
    # Iterate from the bottom up to find the first empty spot
    for row_idx in range(num_rows - 1, -1, -1):
        if board[row_idx][col_index] == " ":
            board[row_idx][col_index] = player_checker
            return True, row_idx
    return False, -1  # Column is full

def check_win(board, player_checker, row, col, connect_n):
    """
    Checks if the current player has won the game by connecting N checkers
    horizontally, vertically, or diagonally, starting from the last placed checker.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol of the current player.
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        connect_n (int): The number of checkers needed to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to count consecutive checkers in a given direction
    def count_direction(r_start, c_start, r_delta, c_delta):
        count = 0
        r, c = r_start, c_start
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == player_checker:
            count += 1
            r += r_delta
            c += c_delta
        return count

    # 1. Check Horizontal
    # Count left from (row, col) and right from (row, col)
    horizontal_count = count_direction(row, col, 0, -1) + count_direction(row, col, 0, 1) - 1
    if horizontal_count >= connect_n:
        return True

    # 2. Check Vertical
    # Count down from (row, col) (no need to check up as checker falls down)
    vertical_count = count_direction(row, col, 1, 0) # Only check downwards
    if vertical_count >= connect_n:
        return True

    # 3. Check Diagonal (top-left to bottom-right)
    # Count up-left from (row, col) and down-right from (row, col)
    diag1_count = count_direction(row, col, -1, -1) + count_direction(row, col, 1, 1) - 1
    if diag1_count >= connect_n:
        return True

    # 4. Check Diagonal (top-right to bottom-left)
    # Count up-right from (row, col) and down-left from (row, col)
    diag2_count = count_direction(row, col, -1, 1) + count_direction(row, col, 1, -1) - 1
    if diag2_count >= connect_n:
        return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False  # Found an empty cell, game is not a draw yet
    return True  # No empty cells found, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles turns, checks for wins/draws, and ends the game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    num_players = NUM_PLAYERS
    player_checkers = CHECKERS

    # Randomly select the first player
    current_player_idx = random.randint(0, num_players - 1)

    game_over = False
    winning_player_checker = None

    while not game_over:
        print_board(board)
        current_player_checker = player_checkers[current_player_idx]

        valid_move = False
        col_chosen = -1
        row_landed = -1

        while not valid_move:
            col_chosen = get_player_input(current_player_checker, NUM_COLS)
            placed, row_landed = drop_checker(board, col_chosen, current_player_checker)

            if placed:
                valid_move = True
            else:
                print(f"Column {chr(ord('A') + col_chosen)} is full. Please choose another column.")
                # Player does not lose turn for choosing a full column

        # After a valid move, check for win or draw
        if check_win(board, current_player_checker, row_landed, col_chosen, CONNECT_N):
            winning_player_checker = current_player_checker
            game_over = True
        elif check_draw(board):
            game_over = True
            winning_player_checker = None # Indicate a draw
        else:
            # Switch to the next player
            current_player_idx = (current_player_idx + 1) % num_players

    # Game over, print final board and result
    print_board(board)
    if winning_player_checker:
        print(f"Player {winning_player_checker} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    main()
