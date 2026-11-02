import os
import random
import string

# Constants (adjustable, but submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

WIN_LENGTH = 4  # Always 4 to win, independent of board size

# Validate constants
if COLS > 26:
    raise ValueError("Maximum of 26 columns supported.")
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    raise ValueError("Number of players must be between 2 and 5.")
PLAYERS = PLAYER_SYMBOLS[:NUM_PLAYERS]


def clear_screen():
    # Clear the terminal screen (Linux/Unix)
    os.system('clear')


def create_board(rows, cols):
    # Create a board filled with single space characters
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column headers (A, B, C, ...)
    headers = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(headers)
    # Top border
    print("+" + ("---+" * cols))
    # Rows
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + ("---+" * cols))


def get_column_from_input(user_input, cols):
    if len(user_input) != 1:
        return None
    ch = user_input.upper()
    if ch < 'A' or ch > chr(ord('A') + cols - 1):
        return None
    return ord(ch) - ord('A')


def drop_checker(board, col_index, checker):
    # Try to place checker in the lowest available cell of the column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r
    return -1  # Column is full


def check_direction(board, start_r, start_c, delta_r, delta_c, checker):
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_r, start_c
    for _ in range(WIN_LENGTH):
        if 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += delta_r
            c += delta_c
        else:
            break
    return count == WIN_LENGTH


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check every position as a potential start
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # Horizontal right
            if c + WIN_LENGTH - 1 < cols and check_direction(board, r, c, 0, 1, checker):
                return True
            # Vertical down
            if r + WIN_LENGTH - 1 < rows and check_direction(board, r, c, 1, 0, checker):
                return True
            # Diagonal down-right
            if r + WIN_LENGTH - 1 < rows and c + WIN_LENGTH - 1 < cols and check_direction(board, r, c, 1, 1, checker):
                return True
            # Diagonal up-right
            if r - (WIN_LENGTH - 1) >= 0 and c + WIN_LENGTH - 1 < cols and check_direction(board, r, c, -1, 1, checker):
                return True
    return False


def check_draw(board):
    # Draw if no empty spaces left on the board
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)

    # Randomly choose starting player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_checker = PLAYERS[current_player_index]
        prompt = f"Player {current_checker}, please enter a column: "
        col_index = None

        # Input validation loop for user entry (characters/out-of-range)
        while True:
            user_input = input(prompt).strip()
            col_index = get_column_from_input(user_input, COLS)
            if col_index is not None:
                break
            print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")

        # Attempt to drop the checker
        row_placed = drop_checker(board, col_index, current_checker)

        # Clear and print updated board
        clear_screen()
        print_board(board)

        if row_placed == -1:
            # Column full: player loses the turn
            print("Column is full. Turn lost.")
        else:
            # Check for win
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            # Check for draw
            if check_draw(board):
                print("It's a draw!")
                break

        # Next player's turn (always alternate, even if turn was lost)
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
