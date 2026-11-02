import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


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
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board


def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()  # Clear screen before printing the updated board

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print the board with separators
    for row in board:
        print("+", end="")
        for _ in row:
            print("---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    # Print the last horizontal separator
    print("+", end="")
    for _ in board[0]:
        print("---+", end="")
    print()


def get_column_input(player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The valid 0-based column index chosen by the player.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not ('A' <= col_char <= chr(ord('A') + num_cols - 1)):
                raise ValueError("Invalid column. Please enter a single uppercase letter within the board range.")

            col_index = ord(col_char) - ord('A')
            return col_index
        except ValueError as e:
            print(f"Error: {e}")
        except EOFError:  # Handle Ctrl+D scenario in some terminals
            print("\nExiting game. Goodbye!")
            exit()


def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        tuple: (True, row_index) if the checker was successfully placed,
               (False, -1) if the column is full.
    """
    for row_index in range(len(board) - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = player_checker
            return True, row_index
    return False, -1  # Column is full


def check_win(board, last_row, last_col, player_checker, win_condition):
    """
    Checks if the last placed checker resulted in a win.

    Args:
        board (list): The 2D list representing the game board.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.
        player_checker (str): The checker symbol of the player who just moved.
        win_condition (int): The number of checkers needed to win.

    Returns:
        bool: True if the player won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Directions for checking (horizontal, vertical, diagonal)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal (top-left to bottom-right)
        (1, -1)   # Diagonal (top-right to bottom-left)
    ]

    for dr, dc in directions:
        count = 0
        # Check in positive direction
        for i in range(win_condition):
            r, c = last_row + i * dr, last_col + i * dc
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == player_checker:
                count += 1
            else:
                break
        # Check in negative direction (if not vertical, as vertical only goes one way from bottom)
        if dr != 1 or dc != 0:  # Only for horizontal and diagonal
            for i in range(1, win_condition):
                r, c = last_row - i * dr, last_col - i * dc
                if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == player_checker:
                    count += 1
                else:
                    break
        if count >= win_condition:
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
                return False  # Found an empty cell, not a draw
    return True  # No empty cells found, it's a draw


def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)  # Randomly choose first player

    game_over = False
    winning_player = None

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        # Get valid column input
        col_index = get_column_input(current_player_checker, NUM_COLS)

        # Attempt to drop checker
        placed, row_index = drop_checker(board, col_index, current_player_checker)

        if not placed:
            print("Column is full! Please choose another column.")
            # Player does not lose turn if column is full, they are prompted again
            # The loop continues, current_player_index does not change
            continue
        else:
            # Check for win condition
            if check_win(board, row_index, col_index, current_player_checker, WIN_CONDITION):
                winning_player = current_player_checker
                game_over = True
            # Check for draw condition
            elif check_draw(board):
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game Over
    print_board(board)  # Print final board state

    if winning_player:
        print(f"Player {winning_player} won!")
    else:
        print("It's a draw!")


# --- Main execution ---
if __name__ == "__main__":
    play_connect_4()
