import os
import random
import sys

# ----- Global Constants -----
# Board dimensions (modifiable up to 26 columns)
ROWS = 6
COLS = 7

# Player settings
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # Can be set between 2 and 5

# Letters for column labels, up to 26 (A-Z)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]


# ----- Functions -----

def clear_screen():
    """Clears the console screen."""
    os.system('clear')


def create_board(rows, cols):
    """Creates an empty board as a 2D list."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Prints the board with column letters on top."""
    clear_screen()
    # Print header with column letters
    print("  " + "   ".join(COLUMN_LABELS[:COLS]))
    # Print horizontal line
    print("+" + "---+" * COLS)
    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)


def get_valid_column_input(board):
    """
    Prompts user for a valid column letter, validates it,
    and returns column index (int).
    """
    while True:
        col_input = input().strip()
        if len(col_input) != 1 or not col_input.isalpha() or not col_input.isupper():
            print("Invalid input. Please enter a single uppercase letter corresponding to a column:")
            continue
        col_index = ord(col_input) - ord('A')
        if col_index < 0 or col_index >= COLS:
            print("Column out of range. Choose a letter between A and {}:".format(COLUMN_LABELS[COLS-1]))
            continue
        # Check if the column is full
        if board[0][col_index] != " ":
            print("Column {} is full. Choose another column:".format(col_input))
            return None  # Signal that turn is lost (column is full)
        return col_index


def place_checker(board, col, player_checker):
    """
    Places the checker in the chosen column at the lowest empty spot.
    Returns the (row, col) where the checker is placed.
    """
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return row, col
    # Should never reach here if validated before usage
    return None, None


def check_win(board, player_checker):
    """Checks for 4 consecutive (horizontal, vertical, diagonal) checkers for the player."""
    # Horizontal, vertical, / diagonal, \ diagonal
    directions = [
        (0, 1),  # right
        (1, 0),  # down
        (1, 1),  # down right
        (1, -1), # down left
    ]
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != player_checker:
                continue
            for dr, dc in directions:
                count = 1
                r, c = row, col
                for _ in range(3):  # Need 3 more steps
                    r += dr
                    c += dc
                    if (0 <= r < ROWS and 0 <= c < COLS) and board[r][c] == player_checker:
                        count += 1
                    else:
                        break
                if count == 4:
                    return True
    return False


def check_draw(board):
    """Checks if the board is completely filled up."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def main():
    # Choose the checkers for the number of players
    player_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    # Randomly select starting player
    curr_player = random.randint(0, NUM_PLAYERS - 1)
    # Create board
    board = create_board(ROWS, COLS)
    print_board(board)
    print("Player {}, please enter a column:".format(player_checkers[curr_player]))

    while True:
        # Read player's input & handle invalid or full input
        col_index = get_valid_column_input(board)
        if col_index is None:
            # If column was full, player loses turn
            curr_player = (curr_player + 1) % NUM_PLAYERS
            print_board(board)
            print("Player {}, please enter a column:".format(player_checkers[curr_player]))
            continue

        # Place checker
        row_index, col_num = place_checker(board, col_index, player_checkers[curr_player])

        # Print the updated board
        print_board(board)

        # Check for win
        if check_win(board, player_checkers[curr_player]):
            print("Player {} won!".format(player_checkers[curr_player]))
            return

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            return

        # Next player's turn
        curr_player = (curr_player + 1) % NUM_PLAYERS
        print("Player {}, please enter a column:".format(player_checkers[curr_player]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Bye!")
        sys.exit()
