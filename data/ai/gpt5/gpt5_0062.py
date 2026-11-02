import os
import random
import string

# Constants (Submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    # Clear the terminal screen (Linux/Unix as required)
    os.system('clear')


def create_board(rows, cols):
    # Create a board initialized with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column headers A..Z
    headers = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(headers))
    print("+" + "---+" * cols)
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + "---+" * cols)


def valid_column_letter(ch, cols):
    if len(ch) != 1:
        return False
    if ch not in string.ascii_uppercase:
        return False
    index = ord(ch) - ord('A')
    return 0 <= index < cols


def get_column_index(cols):
    # Keep asking until a valid column letter within board range is given
    while True:
        user_input = input().strip()
        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue
        letter = user_input[0].upper()
        if not valid_column_letter(letter, cols):
            print("Invalid input. Please enter a valid column letter within the board.")
            continue
        return ord(letter) - ord('A')


def drop_checker(board, col, checker):
    # Place checker in the lowest available row in the given column
    # Return True if successful, False if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r][c + 1] == checker and
                board[r][c + 2] == checker and
                board[r][c + 3] == checker):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - 3):
            if (board[r][c] == checker and
                board[r + 1][c] == checker and
                board[r + 2][c] == checker and
                board[r + 3][c] == checker):
                return True

    # Diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r + 1][c + 1] == checker and
                board[r + 2][c + 2] == checker and
                board[r + 3][c + 3] == checker):
                return True

    # Diagonal up-right
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r - 1][c + 1] == checker and
                board[r - 2][c + 2] == checker and
                board[r - 3][c + 3] == checker):
                return True

    return False


def check_draw(board):
    # Draw if no spaces remain
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    # Setup
    cols = max(1, min(COLS, 26))  # Enforce max 26 columns
    rows = ROWS
    num_players = max(2, min(NUM_PLAYERS, 5))
    players = CHECKERS[:num_players]

    board = create_board(rows, cols)

    # Randomly select first player
    current_player_index = random.randint(0, num_players - 1)

    # Initial board print before game starts
    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_index]}, please enter a column:")

    # Game loop
    while True:
        # Get a valid column letter within the board
        col = get_column_index(cols)

        # Attempt to drop checker
        checker = players[current_player_index]
        placed = drop_checker(board, col, checker)

        # After each turn (even if invalid due to full column), print board
        clear_screen()
        print_board(board)

        if not placed:
            # Column full: turn is invalid and player loses the turn
            print(f"Column {string.ascii_uppercase[col]} is full. Player {checker} loses the turn.")
        else:
            # Check for win
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break

            # Check for draw
            if check_draw(board):
                print("It's a draw!")
                break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players
        print(f"Player {players[current_player_index]}, please enter a column:")


if __name__ == "__main__":
    main()
