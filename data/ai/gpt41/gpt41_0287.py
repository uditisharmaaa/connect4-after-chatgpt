import os
import random
import string

# ===== CONSTANTS ===== #
ROWS = 6           # Number of rows
COLS = 7           # Number of columns (max 26)
PLAYERS = 2        # Number of players (2-5)
CHECKERS = ["X", "O", "V", "H", "M"]

EMPTY_CELL = " "   # Symbol for empty cell

# ===== FUNCTION DEFINITIONS ===== #

def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    """Initializes a 2D board."""
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Prints the current state of the board, including column labels."""
    clear_screen()
    columns_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    header = "  " + "   ".join(columns_labels)
    separator = "+" + "---+" * len(board[0])
    print(header)
    print(separator)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(separator)


def get_valid_columns(board):
    """Returns a set of valid column indices that are not yet full."""
    valid_cols = set()
    cols = len(board[0])
    for col in range(cols):
        if board[0][col] == EMPTY_CELL:
            valid_cols.add(col)
    return valid_cols


def get_player_input(board):
    """Prompts the player for a valid column and returns the zero-based column index."""
    valid_columns = get_valid_columns(board)
    cols = len(board[0])
    columns_labels = [chr(ord('A') + i) for i in range(cols)]
    while True:
        choice = input("Please enter a column: ").strip().upper()
        if len(choice) != 1 or choice not in columns_labels:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_idx = ord(choice) - ord('A')
        if col_idx not in valid_columns:
            print("That column is full or invalid. Try another column.")
            continue
        return col_idx


def place_checker(board, col, checker):
    """Places the checker in the lowest available cell in the column."""
    for row in reversed(range(len(board))):
        if board[row][col] == EMPTY_CELL:
            board[row][col] = checker
            return row, col
    return None  # Column full (shouldn't happen if input is validated)


def check_victory(board, last_row, last_col, checker):
    """Checks if the player has won after placing a checker."""
    # Directions: (dr, dc)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check the other direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False


def check_draw(board):
    """Checks if the board is full."""
    return all(cell != EMPTY_CELL for cell in board[0])


def next_player(current, num_players):
    """Returns the index of the next player."""
    return (current + 1) % num_players


def main():
    # Set up board and players
    board = create_board(ROWS, COLS)
    num_players = PLAYERS
    players = CHECKERS[:num_players]

    # Random starting player
    current_player_idx = random.randint(0, num_players - 1)

    print_board(board)
    print(f"Player {players[current_player_idx]} will start!\n(Press Enter to begin)")
    input()

    # Main game loop
    move_count = 0
    while True:
        print_board(board)
        player_checker = players[current_player_idx]
        print(f"Player {player_checker}, ", end="")
        col_choice = get_player_input(board)
        position = place_checker(board, col_choice, player_checker)
        move_count += 1

        if position is None:
            # Should not get here due to input validation, but if so, skip turn
            print("Column is full! Turn lost.")
        else:
            row, col = position
            # Check for victory
            if check_victory(board, row, col, player_checker):
                print_board(board)
                print(f"Player {player_checker} won!")
                break

            # Check for draw
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

        # Next player's turn
        current_player_idx = next_player(current_player_idx, num_players)


# Entry point
if __name__ == "__main__":
    main()
