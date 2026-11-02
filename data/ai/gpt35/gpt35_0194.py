import os
import random

# ----- CONSTANTS -----
ROWS = 6               # Number of rows
COLUMNS = 7            # Number of columns (max 26)
NUM_PLAYERS = 2        # Number of players (2 to 5)
WIN_CONDITION = 4      # Number of consecutive checkers needed to win

# Player checkers in order
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def create_board(rows, columns):
    """
    Create a board with specified rows and columns.
    The board is a list of lists filled with " " (empty space).
    """
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """
    Print the Connect 4 board with column labels and borders.
    """
    clear_screen()
    # Print column labels (A, B, C, ...)
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))

    # Print board rows with cell separators and horizontal borders
    for row in range(len(board)):
        print("+" + "---+" * len(board[0]))
        # Print a row of cells
        row_line = "|"
        for col in range(len(board[0])):
            row_line += " " + board[row][col] + " |"
        print(row_line)
    print("+" + "---+" * len(board[0]))


def random_start_player(num_players):
    """
    Return index of a random player to start.
    """
    return random.randint(0, num_players - 1)


def valid_input(column_input, board):
    """
    Check if the column input is valid:
    - Single uppercase letter
    - Within board columns
    """
    if len(column_input) != 1:
        return False
    if not ('A' <= column_input <= chr(ord('A') + len(board[0]) - 1)):
        return False
    return True


def column_index(column_char):
    """
    Convert column label letter to integer index.
    """
    return ord(column_char) - ord('A')


def place_checker(board, col_idx, checker):
    """
    Place the checker in the lowest available row in the given column.
    Returns True if checker was placed successfully, False if column is full.
    """
    # Start checking from bottom row upwards
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False  # Column full


def check_win(board, checker):
    """
    Check board for 4 consecutive checkers (WIN_CONDITION) for the given player:
    horizontal, vertical, and both diagonal directions.
    Returns True if player won, else False.
    """
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False


def check_draw(board):
    """
    Check if the board is completely filled (no empty spaces).
    If so and no winner, it is a draw.
    """
    for row in board:
        if " " in row:
            return False
    return True


def main():
    # Initialize board and players
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_player = random_start_player(NUM_PLAYERS)

    # Print initial board
    print_board(board)

    # Main game loop
    while True:
        current_checker = players[current_player]

        # Prompt player input until valid or column is full
        while True:
            prompt = f"Player {current_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not valid_input(user_input, board):
                # Invalid input, ask again without losing turn
                continue

            col = column_index(user_input)
            placed = place_checker(board, col, current_checker)

            if not placed:
                # Column full => lose turn immediately
                break
            else:
                # Checker placed successfully, break input loop
                break

        # Print updated board
        print_board(board)

        if placed:
            # Check if current player won
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            # Check for draw
            if check_draw(board):
                print("The game is a draw!")
                break

        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
