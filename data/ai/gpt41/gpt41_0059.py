import os
import random
import string
import sys

# ----------- Constants -----------
NUM_ROWS = 6
NUM_COLS = 7         # Max 26
NUM_PLAYERS = 2      # Between 2 and 5, as per assignment

# Supported player checkers in order
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    # Clear the screen
    os.system('clear')


def create_board(rows, cols):
    # Create 2D board with all cells as whitespace
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column labels (A, B, ...)
    top_labels = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(top_labels)
    print("+" + "---+" * cols)
    for row in board:
        # Print each row
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)


def get_valid_column_input(board):
    cols = len(board[0])
    valid_columns = string.ascii_uppercase[:cols]
    while True:
        user_in = input("Please enter a column: ").strip().upper()
        # Input validation
        if len(user_in) != 1 or user_in not in valid_columns:
            print("Invalid input. Please enter a valid column letter (A-{}).".format(valid_columns[-1]))
            continue
        col_idx = ord(user_in) - ord('A')
        # Check if the column is full
        if board[0][col_idx] != " ":
            print("Column {} is full! You lose your turn.".format(user_in))
            return None  # Indicate turn is lost
        return col_idx


def place_checker(board, col, checker):
    # Place checker in lowest available spot in column
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Shouldn't happen if checked prior


def check_win(board, checker):
    rows, cols = len(board), len(board[0])
    directions = [
        (0, 1),  # Horizontal right
        (1, 0),  # Vertical down
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                win = True
                for k in range(1, 4):
                    nr, nc = r + dr*k, c + dc*k
                    if nr < 0 or nr >= rows or nc < 0 or nc >= cols or board[nr][nc] != checker:
                        win = False
                        break
                if win:
                    return True
    return False


def check_draw(board):
    # If there are any blank spaces in top row, no draw
    return all(cell != " " for cell in board[0])


def main():
    # Set up for assignment requirements
    board = create_board(NUM_ROWS, NUM_COLS)
    # Only support number of players allowed (2-5)
    assert 2 <= NUM_PLAYERS <= 5
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Pick first player at random
    current_player_idx = random.randrange(NUM_PLAYERS)
    print_board(board)
    print("Players: " + ", ".join(players))
    print("First player chosen at random is '{}'.".format(players[current_player_idx]))
    input("Press Enter to start the game...")

    while True:
        print_board(board)
        current_checker = players[current_player_idx]
        print("Player {}, your turn.".format(current_checker))
        col_idx = get_valid_column_input(board)
        if col_idx is None:
            # Turn is lost (column full)
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue
        row, col = place_checker(board, col_idx, current_checker)
        # After placing, check if this player has won
        if check_win(board, current_checker):
            print_board(board)
            print("Player {} won!".format(current_checker))
            break
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        # Next turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated. Goodbye!")
        sys.exit(0)
