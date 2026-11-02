import os
import random
import string

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_CONDITION = 4
PLAYERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    # Create a board filled with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column letters
    letters = string.ascii_uppercase[:cols]
    print("  " + "   ".join(letters))
    line = "+---" * cols + "+"
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)


def is_valid_column(col_ch, cols):
    return col_ch in string.ascii_uppercase[:cols]


def get_column_index(col_ch):
    return string.ascii_uppercase.index(col_ch)


def place_checker(board, col_i, checker):
    # Place checker in lowest empty space in col_i, from bottom.
    # Return True if placed, False if column full.
    for row_i in range(len(board) - 1, -1, -1):
        if board[row_i][col_i] == " ":
            board[row_i][col_i] = checker
            return True
    return False


def is_board_full(board):
    # Board full if no empty space in top row
    return all(cell != " " for cell in board[0])


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_CONDITION:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_CONDITION:
                    return True
            else:
                count = 0

    # Diagonal checks
    # Positive slope (/)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            match = True
            for i in range(WIN_CONDITION):
                if board[r - i][c + i] != checker:
                    match = False
                    break
            if match:
                return True

    # Negative slope (\)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            match = True
            for i in range(WIN_CONDITION):
                if board[r + i][c + i] != checker:
                    match = False
                    break
            if match:
                return True

    return False


def main():
    rows = ROWS
    cols = COLS
    num_players = 2  # fixed per assignment instructions

    board = create_board(rows, cols)
    players = PLAYERS[:num_players]

    current_player_idx = random.randint(0, num_players - 1)
    print_board(board)

    while True:
        checker = players[current_player_idx]
        print(f"Player {checker}, please enter a column:")

        player_lost_turn = False
        while True:
            user_input = input().strip().upper()
            if not user_input or len(user_input) != 1:
                print("Invalid input. Please enter a single column letter:")
                continue
            if not is_valid_column(user_input, cols):
                print("Invalid column. Please enter a valid column letter:")
                continue
            col_i = get_column_index(user_input)
            # Try to place checker in column
            if place_checker(board, col_i, checker):
                break
            else:
                # Column full, player loses turn (no retries)
                print(f"Column {user_input} is full. You lose your turn.")
                player_lost_turn = True
                break

        print_board(board)

        # If placed checker (not lost turn), check win
        if not player_lost_turn:
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break

        # Check draw
        if is_board_full(board):
            print("The game is a draw.")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % num_players


if __name__ == "__main__":
    main()
