import os
import random

# --- Global Constants ---
NUM_ROWS = 6  # Number of rows on the board
NUM_COLS = 7  # Number of columns on the board (max 26 for A-Z labeling)
NUM_PLAYERS = 2  # Number of players (2 to 5)
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Column labels (A, B, C, ...)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]


def create_board():
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Returns:
        list: A 2D list representing the game board.
    """
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]


def print_board(board):
    """
    Clears the screen and prints the current state of the Connect 4 board.

    Args:
        board (list): The 2D list representing the game board.
    """
    os.system('clear')  # Clear the terminal screen

    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    for r in range(NUM_ROWS):
        # Print top border for each row
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    # Print bottom border for the last row
    print("+---" * NUM_COLS + "+")


def is_valid_column_input(column_input):
    """
    Checks if the user's column input is valid (a single uppercase letter
    within the range of available columns).

    Args:
        column_input (str): The user's input for the column.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    if not isinstance(column_input, str) or len(column_input) != 1:
        return False
    if column_input.upper() not in COLUMN_LABELS:
        return False
    return True


def get_column_index(column_input):
    """
    Converts a column letter (e.g., 'A') to its corresponding 0-based index.

    Args:
        column_input (str): The column letter.

    Returns:
        int: The 0-based index of the column.
    """
    return COLUMN_LABELS.index(column_input.upper())


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False  # Column is full


def check_win(board, checker):
    """
    Checks if the current player (with 'checker') has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """

    # Helper function to check a specific direction
    def check_direction(r, c, dr, dc):
        count = 0
        for i in range(WIN_CONDITION):
            nr, nc = r + i * dr, c + i * dc
            if 0 <= nr < NUM_ROWS and 0 <= nc < NUM_COLS and board[nr][nc] == checker:
                count += 1
            else:
                break
        return count >= WIN_CONDITION

    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == checker:
                # Check horizontal (right)
                if check_direction(r, c, 0, 1):
                    return True
                # Check vertical (down)
                if check_direction(r, c, 1, 0):
                    return True
                # Check diagonal (down-right)
                if check_direction(r, c, 1, 1):
                    return True
                # Check diagonal (down-left)
                if check_direction(r, c, 1, -1):
                    return True
    return False


def check_draw(board):
    """
    Checks if the board is completely full, resulting in a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw


def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner_checker = None

    while not game_over:
        current_checker = CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        valid_turn = False
        while not valid_turn:
            user_input = input().strip()

            if not is_valid_column_input(user_input):
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C).")
                continue

            col_index = get_column_index(user_input)

            if not drop_checker(board, col_index, current_checker):
                print(f"Column {user_input.upper()} is full. Please choose another column.")
            else:
                valid_turn = True

        # After a valid turn, check for win or draw
        if check_win(board, current_checker):
            winner_checker = current_checker
            game_over = True
        elif check_draw(board):
            game_over = True
            # No winner, it's a draw

        # Switch to the next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game over, print final board and result
    print_board(board)
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("The game is a draw!")


if __name__ == "__main__":
    main()
