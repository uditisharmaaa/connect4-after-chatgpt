import os
import random

# Constants (you can change these for testing; final submission should be 6x7 and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Player checker symbols in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def clear_screen():
    # Clear the terminal screen (Linux/Unix)
    os.system('clear')


def create_board(rows, cols):
    # Create a board filled with spaces
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))

    # Separator
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(sep)


def is_board_full(board):
    # Board is full if no space in top row of any column
    cols = len(board[0])
    rows = len(board)
    for c in range(cols):
        if board[0][c] == ' ':
            return False
    return True


def drop_checker(board, col_index, checker):
    # Try to drop a checker into the given column
    # Return True if placed, False if column is full
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return True
    return False  # Column full


def valid_column_input(user_input, cols):
    # Valid if it's a single alphabetic character within A .. A+cols-1
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    letter = user_input.upper()
    start = ord('A')
    idx = ord(letter) - start
    return 0 <= idx < cols


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    target = checker

    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == target and
                board[r][c + 1] == target and
                board[r][c + 2] == target and
                board[r][c + 3] == target):
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - 3):
            if (board[r][c] == target and
                board[r + 1][c] == target and
                board[r + 2][c] == target and
                board[r + 3][c] == target):
                return True

    # Diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == target and
                board[r + 1][c + 1] == target and
                board[r + 2][c + 2] == target and
                board[r + 3][c + 3] == target):
                return True

    # Diagonal up-right
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == target and
                board[r - 1][c + 1] == target and
                board[r - 2][c + 2] == target and
                board[r - 3][c + 3] == target):
                return True

    return False


def main():
    # Prepare game
    cols = min(COLS, 26)
    rows = ROWS
    num_players = max(2, min(NUM_PLAYERS, 5))
    players = CHECKERS[:num_players]

    board = create_board(rows, cols)

    # Randomly choose starting player index
    current_player_idx = random.randint(0, num_players - 1)

    # Initial board print
    print_board(board)

    while True:
        # Check for draw before asking (board may already be full)
        if is_board_full(board):
            print("It's a draw!")
            break

        current_checker = players[current_player_idx]
        # Prompt for input
        user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        # Validate input (retry until valid character within range)
        while not valid_column_input(user_input, cols):
            print("Invalid input. Please enter a valid column letter.")
            user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        col_index = ord(user_input) - ord('A')

        # Try to place checker
        placed = drop_checker(board, col_index, current_checker)

        # Print updated board after action (successful or not)
        print_board(board)

        if not placed:
            # Column full: turn is invalid and player loses the turn
            print(f"Column {user_input} is full. Turn lost.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % num_players
            continue

        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players


if __name__ == "__main__":
    main()
