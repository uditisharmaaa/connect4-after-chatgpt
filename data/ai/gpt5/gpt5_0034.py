import os
import random
import sys

# Constants (submission requires 6 rows x 7 columns and 2 players)
NUM_ROWS = 6
NUM_COLS = 7  # Must be <= 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5

# Player checkers in order
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Win condition (always 4 in a row)
WIN_LENGTH = 4


def clear_screen():
    # Clear terminal screen (Linux/Unix)
    os.system('clear')


def create_board(rows, cols):
    # Create a rows x cols board filled with spaces
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Clear and print the board with column labels A..,
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)

    # Top border
    border = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(border)
        # Print row cells
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(border)


def get_players(num_players):
    # Return list of player symbols based on number of players
    if not (2 <= num_players <= 5):
        raise ValueError("Number of players must be between 2 and 5.")
    return PLAYER_CHECKERS[:num_players]


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def apply_move(board, col_index, checker):
    # Attempt to place checker in the given column.
    # Returns the row index where placed, or None if column is full.
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return r
    return None  # Column full


def check_win(board, last_row, last_col, checker):
    # Check for WIN_LENGTH in a row including last move position.
    # Directions: horizontal, vertical, diagonal down-right, diagonal up-right
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # Start with last placed checker
        # Check forward direction
        r, c = last_row + dr, last_col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = last_row - dr, last_col - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    # Draw if no spaces remain in the top row (board full)
    top_row = board[0]
    return all(cell != ' ' for cell in top_row)


def get_valid_column_input(cols):
    # Prompt until user provides a valid column letter within range A..A+cols-1
    while True:
        user_input = input().strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        ch = user_input[0]
        if not ('A' <= ch <= 'Z'):
            print("Invalid input. Please enter a letter (A-Z).")
            continue
        col_index = ord(ch) - ord('A')
        if not (0 <= col_index < cols):
            max_letter = chr(ord('A') + cols - 1)
            print(f"Invalid input. Please enter a column letter between A and {max_letter}.")
            continue
        return col_index, ch


def main():
    # Validate column limit
    if NUM_COLS > 26:
        print("Error: Maximum supported number of columns is 26.")
        sys.exit(1)

    # Initialize players and board
    players = get_players(NUM_PLAYERS)
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select starting player
    current_player_idx = random.randrange(len(players))

    # Initial board print
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_idx]
        # Prompt
        max_letter = chr(ord('A') + NUM_COLS - 1)
        print(f"Player {current_checker}, please enter a column:", end=" ")

        # Get validated column input (letter within range)
        col_index, col_letter = get_valid_column_input(NUM_COLS)

        # Try to apply the move
        placed_row = apply_move(board, col_index, current_checker)

        # Print updated board after attempt (whether successful or not)
        print_board(board)

        if placed_row is None:
            # Column full -> turn lost
            print(f"Column {col_letter} is full. Player {current_checker} loses the turn.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % len(players)
            continue

        # Check for win
        if check_win(board, placed_row, col_index, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("Game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % len(players)


if __name__ == "__main__":
    main()
