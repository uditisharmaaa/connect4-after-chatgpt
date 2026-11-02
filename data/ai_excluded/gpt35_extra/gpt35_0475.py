import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # Max columns: A-Z
MIN_PLAYERS = 2
MAX_PLAYERS = 5

NUM_PLAYERS = 2  # Set to 2 on submission as requested
CHECKERS = ["X", "O", "V", "H", "M"]  # Ordered checkers for players

WIN_LENGTH = 4  # Number of checkers in a row needed to win


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    # Creates a rows x columns board filled with " "
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    columns = len(board[0])
    rows = len(board)
    # Print column labels
    labels = [chr(ord("A") + i) for i in range(columns)]
    print("  " + "   ".join(labels))
    # Print top border
    print("+---" * columns + "+")
    for r in range(rows):
        print("| " + " | ".join(board[r]) + " |")
        print("+---" * columns + "+")


def input_column(player_checker, columns):
    # Ask player to enter a valid column letter (uppercase)
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            print(f"Invalid input. Please enter a single letter between A and {chr(ord('A') + columns - 1)}.")
            continue
        if not ("A" <= col_input <= chr(ord("A") + columns - 1)):
            print(f"Invalid column letter. Please enter a letter between A and {chr(ord('A') + columns - 1)}.")
            continue
        return ord(col_input) - ord("A")


def place_checker(board, col, checker):
    # Place the checker in the lowest empty row in the specified column
    # Returns True if placed, False if column full.
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False


def board_full(board):
    # Check if the board is full (no empty spaces)
    return all(cell != " " for row in board for cell in row)


def main():
    # Setup game parameters (only 2 players and 6x7 dimensions on submission)
    rows = ROWS
    cols = COLUMNS
    num_players = NUM_PLAYERS
    players = CHECKERS[:num_players]

    board = create_board(rows, cols)

    # Randomly select first player index
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]

        col = input_column(current_checker, cols)

        placed = place_checker(board, col, current_checker)

        if not placed:
            # Column full, player loses turn
            print(f"Column {chr(ord('A') + col)} is full. Player {current_checker} loses the turn.")
            current_player_index = (current_player_index + 1) % num_players
            print_board(board)
            continue

        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("Game is a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players


if __name__ == "__main__":
    main()
