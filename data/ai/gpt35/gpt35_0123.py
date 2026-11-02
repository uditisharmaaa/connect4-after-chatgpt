import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # To handle max 26 columns (A-Z)
PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players supported


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])

    # Print column headers (A, B, C, ...)
    header = "  "
    for c in range(cols):
        header += f"  {chr(ord('A') + c)} "
    print(header)

    # Print separator line
    sep = "+" + "---+" * cols

    for r in range(len(board)):
        print(sep)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(sep)


def valid_column_input(s, cols):
    if len(s) != 1:
        return False
    if not s.isalpha():
        return False
    col_index = ord(s.upper()) - ord('A')
    if 0 <= col_index < cols:
        return True
    return False


def column_full(board, col):
    # If top row in this column is occupied, column is full
    return board[0][col] != " "


def place_checker(board, col, checker):
    # Place checker in lowest empty row in the specified column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full, cannot place
    return None


def has_won(board, checker, r, c):
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1

        # Check in the positive direction
        rr, cc = r + dr, c + dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc

        # Check in the negative direction
        rr, cc = r - dr, c - dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr -= dr
            cc -= dc

        if count >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    # Draw if no empty spaces in top row (which means no moves left)
    return all(cell != " " for cell in board[0])


def next_player_index(current, player_count):
    return (current + 1) % player_count


def main():
    rows, cols = ROWS, COLUMNS
    player_count = PLAYERS
    players = CHECKERS[:player_count]

    board = create_board(rows, cols)

    # Random first player
    current_player_i = random.randrange(player_count)

    print_board(board)

    while True:
        current_checker = players[current_player_i]
        prompt = f"Player {current_checker}, please enter a column: "

        # Input loop with validation
        while True:
            col_input = input(prompt).strip().upper()
            if not valid_column_input(col_input, cols):
                continue
            col = ord(col_input) - ord('A')
            if column_full(board, col):
                # According to spec: "If the column is already completely filled with checkers,
                # the turn is invalid and the player loses the turn."
                # We do not reprompt, so break and lose turn.
                break
            # Valid input and column not full
            placed = place_checker(board, col, current_checker)
            if placed is not None:
                r, c = placed
                break
        else:
            # Should never reach here due to breaks on continue and lose turn logic
            pass

        print_board(board)

        # If player placed checker (not lost turn)
        if not column_full(board, col):
            if placed is not None:
                if has_won(board, current_checker, r, c):
                    print(f"Player {current_checker} won!")
                    break
            else:
                # No checker placed - player lost turn by choosing full column
                pass

        # Check draw
        if is_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_i = next_player_index(current_player_i, player_count)


if __name__ == "__main__":
    main()
