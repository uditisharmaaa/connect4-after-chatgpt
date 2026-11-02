import os
import random
import string

# Constants for board dimensions and players
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Players' checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Use only the number of players and board dimensions required by submission instructions:
NUM_PLAYERS = 2  # must be between MIN_PLAYERS and MAX_PLAYERS inclusive
WIN_COUNT = 4    # number of checkers in a row needed to win


def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


def create_board(rows, cols):
    # Create a board as a list of lists filled with " " (space)
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()

    cols = len(board[0])
    rows = len(board)

    # Print column headers (letters)
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)

    # Print top border of board
    print("+" + "---+" * cols)

    # Print each row of the board
    for r in range(rows):
        # print row cells
        row_string = "| " + " | ".join(board[r]) + " |"
        print(row_string)
        # print row separator
        print("+" + "---+" * cols)


def is_valid_column(col_char, cols, board):
    if col_char not in string.ascii_uppercase[:cols]:
        return False
    col_index = ord(col_char) - ord('A')
    # Check if top cell in the column is empty (means column not full)
    return board[0][col_index] == " "


def get_column_index(col_char):
    return ord(col_char) - ord('A')


def place_checker(board, col_index, checker):
    # Place checker in the lowest available row in the column
    rows = len(board)
    # iterate from bottom row upwards
    for r in reversed(range(rows)):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r, col_index
    # Column full, no place to put checker
    return None


def check_win(board, r, c, checker):
    rows, cols = len(board), len(board[0])

    def count_direction(delta_r, delta_c):
        count = 0
        row, col = r + delta_r, c + delta_c
        while 0 <= row < rows and 0 <= col < cols and board[row][col] == checker:
            count += 1
            row += delta_r
            col += delta_c
        return count

    # Horizontal (left + right)
    total = 1 + count_direction(0, -1) + count_direction(0, 1)
    if total >= WIN_COUNT:
        return True

    # Vertical (up + down)
    total = 1 + count_direction(-1, 0) + count_direction(1, 0)
    if total >= WIN_COUNT:
        return True

    # Diagonal (top-left to bottom-right)
    total = 1 + count_direction(-1, -1) + count_direction(1, 1)
    if total >= WIN_COUNT:
        return True

    # Diagonal (top-right to bottom-left)
    total = 1 + count_direction(-1, 1) + count_direction(1, -1)
    if total >= WIN_COUNT:
        return True

    return False


def is_draw(board):
    # If no empty spaces on top row, board is full => draw
    # Because if one space empty, a checker can be placed
    return all(cell != " " for cell in board[0])


def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        cols_letters = string.ascii_uppercase[:COLS]

        prompt = f"Player {current_checker}, please enter a column: "

        # Input loop until valid input or lose turn if column full
        while True:
            col_input = input(prompt).strip().upper()

            # Validate input length and character
            if len(col_input) != 1 or col_input not in cols_letters:
                # Invalid character or out of board range
                print("Invalid input. Please enter a valid column letter.")
                continue

            col_idx = get_column_index(col_input)

            if board[0][col_idx] != " ":
                # Column is full, lose turn
                # Inform player and break to next player
                print(f"Column {col_input} is full. Player {current_checker} loses the turn.")
                break

            # Place checker and break to next steps
            pos = place_checker(board, col_idx, current_checker)
            if pos is not None:
                break
            else:
                # Should not happen because we checked top cell, but guard anyway
                print(f"Column {col_input} is full. Player {current_checker} loses the turn.")
                break

        print_board(board)

        # If placed successfully, check win and draw
        if pos is not None:
            r, c = pos
            if check_win(board, r, c, current_checker):
                print(f"Player {current_checker} won!")
                return

            if is_draw(board):
                print("The game is a draw!")
                return

        # Next player's turn (regardless of lost turn or played move)
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
