import os
import random
import string

# ====== CONSTANTS ======
# Board dimensions (ROWS x COLUMNS)
ROWS = 6
COLUMNS = 7
# Players (Change PLAYER_COUNT to support 2-5 players)
PLAYER_COUNT = 2  # Set to 2 for submission, can be changed up to 5
CHECKERS = ["X", "O", "V", "H", "M"]
# How many in a row to win
CONNECT_N = 4


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    cols = len(board[0])
    # Print column headers
    headers = ""
    for i in range(cols):
        headers += "  " + chr(ord('A') + i) + " "
    print(headers)
    print("+" + "---+" * cols)
    # Print rows
    for row in board:
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
        print("+" + "---+" * cols)


def get_available_row(board, col):
    # Return the bottom-most empty row in col (or None if col full)
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return None


def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - CONNECT_N + 1):
            if all(board[r][c + i] == checker for i in range(CONNECT_N)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - CONNECT_N + 1):
            if all(board[r + i][c] == checker for i in range(CONNECT_N)):
                return True

    # Diagonal (\) check
    for r in range(rows - CONNECT_N + 1):
        for c in range(cols - CONNECT_N + 1):
            if all(board[r + i][c + i] == checker for i in range(CONNECT_N)):
                return True

    # Diagonal (/) check
    for r in range(CONNECT_N - 1, rows):
        for c in range(cols - CONNECT_N + 1):
            if all(board[r - i][c + i] == checker for i in range(CONNECT_N)):
                return True

    return False


def get_valid_column(input_str, board):
    # Remove whitespace and uppercase
    input_str = input_str.strip().upper()
    if len(input_str) != 1:
        return None
    col_letter = input_str[0]
    valid_letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    if col_letter not in valid_letters:
        return None
    col = ord(col_letter) - ord('A')
    return col


def main():
    board = create_board(ROWS, COLUMNS)
    player_checkers = CHECKERS[:PLAYER_COUNT]
    current = random.randint(0, PLAYER_COUNT - 1)  # Random first player

    # Start game
    while True:
        clear_screen()
        print_board(board)
        checker = player_checkers[current]
        print(f"Player {checker}, please enter a column:")

        user_input = input()
        col = get_valid_column(user_input, board)
        # Input validation
        while col is None or get_available_row(board, col) is None:
            if col is None:
                print("Invalid input. Please enter a valid column letter (A-G).")
            else:
                print("Column is full. You lose your turn!")
                # Skip turn if column full
                current = (current + 1) % PLAYER_COUNT
                break

            user_input = input()
            col = get_valid_column(user_input, board)

        # Column full: skip placement
        if col is None or get_available_row(board, col) is None:
            continue

        # Place checker
        row = get_available_row(board, col)
        board[row][col] = checker

        # Check for win
        if check_win(board, checker):
            clear_screen()
            print_board(board)
            print(f"Player {checker} won!")
            break

        # Check for draw
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player
        current = (current + 1) % PLAYER_COUNT


if __name__ == "__main__":
    main()
