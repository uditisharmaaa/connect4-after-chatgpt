import os
import random

# Global constants for board dimensions and player settings
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels
NUM_PLAYERS = 2  # Between 2 and 5 players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
EMPTY_CELL = " "

def create_board(rows, cols):
    """
    Creates and returns a 2D list representing the game board,
    initialized with empty cells.
    """
    board = []
    for _ in range(rows):
        board.append([EMPTY_CELL] * cols)
    return board

def print_board(board):
    """
    Clears the screen and prints the current state of the game board
    with column labels.
    """
    os.system('clear')  # Clear the terminal screen

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print the board with separators
    for row_index in range(len(board)):
        print("+---+", end="")
        for _ in range(len(board[0]) - 1):
            print("---+", end="")
        print()

        print("|", end="")
        for col_index in range(len(board[0])):
            print(f" {board[row_index][col_index]} |", end="")
        print()

    # Print the bottom separator
    print("+---+", end="")
    for _ in range(len(board[0]) - 1):
        print("---+", end="")
    print()

def get_player_input(current_player_checker, board):
    """
    Prompts the current player for a column input, validates it,
    and returns the 0-indexed column number.
    Keeps asking until a valid and available column is provided.
    """
    num_cols = len(board[0])
    while True:
        player_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

        if len(player_input) != 1:
            print("Invalid input. Please enter a single letter (e.g., A, B).")
            continue

        col_char = player_input[0]
        if not 'A' <= col_char <= chr(ord('A') + num_cols - 1):
            print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + num_cols - 1)}.")
            continue

        col_index = ord(col_char) - ord('A')

        # Check if the column is full
        if board[0][col_index] != EMPTY_CELL:
            print(f"Column {col_char} is full. Please choose another column.")
            continue

        return col_index

def drop_checker(board, col_index, checker):
    """
    Places the given checker in the lowest available row of the specified column.
    Returns the row index where the checker was placed.
    Assumes the column is not full (checked by get_player_input).
    """
    num_rows = len(board)
    for row_index in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == EMPTY_CELL:
            board[row_index][col_index] = checker
            return row_index
    return -1 # Should not happen if column full check is done before calling

def check_win(board, checker, last_row, last_col):
    """
    Checks if the current player (with 'checker') has won after placing
    a checker at (last_row, last_col).
    Checks horizontally, vertically, and both diagonals.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(num_cols):
        if board[last_row][c] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(num_rows):
        if board[r][last_col] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0

    # Check ascending diagonal (bottom-left to top-right)
    count = 0
    # Find the start of the diagonal from the last placed checker
    start_row = last_row
    start_col = last_col
    while start_row < num_rows - 1 and start_col > 0:
        start_row += 1
        start_col -= 1

    r, c = start_row, start_col
    while r >= 0 and c < num_cols:
        if board[r][c] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1

    # Check descending diagonal (top-left to bottom-right)
    count = 0
    # Find the start of the diagonal from the last placed checker
    start_row = last_row
    start_col = last_col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1

    r, c = start_row, start_col
    while r < num_rows and c < num_cols:
        if board[r][c] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
        r += 1
        c += 1

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for row in board:
        for cell in row:
            if cell == EMPTY_CELL:
                return False
    return True

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner_found = False

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        col_index = get_player_input(current_player_checker, board)
        last_row = drop_checker(board, col_index, current_player_checker)
        last_col = col_index

        if check_win(board, current_player_checker, last_row, last_col):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            winner_found = True
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
