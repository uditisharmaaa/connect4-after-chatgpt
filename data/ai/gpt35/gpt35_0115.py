import os
import random
import string

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    cols = len(board[0])
    # Print column headers
    letters = string.ascii_uppercase
    print("  " + "   ".join(letters[:cols]))
    print("+---" * cols + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * cols + "+")


def get_valid_input(player, cols, board):
    cols_letters = string.ascii_uppercase[:cols]
    while True:
        col = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col) != 1 or col not in cols_letters:
            print("Invalid input. Please enter a valid column letter.")
            continue

        col_idx = cols_letters.index(col)

        # Check if the column is full
        if board[0][col_idx] != " ":
            # Column full: player loses turn (invalid move)
            print(f"Column {col} is full. You lose your turn.")
            return None
        return col_idx


def place_checker(board, col_idx, checker):
    # Place checker at lowest empty place in the column
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    # Should not happen as place is already checked full
    return None, None


def check_win(board, checker, row, col):
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1

        # Count in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Count in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True
    return False


def check_draw(board):
    # Draw if no empty spaces in top row (board full)
    return all(cell != " " for cell in board[0])


def main():
    rows, cols = ROWS, COLS
    num_players = 2  # per assignment submission requirement

    board = create_board(rows, cols)

    players = CHECKERS[:num_players]

    # Randomly select first player
    current_player_idx = random.randint(0, num_players - 1)

    clear_screen()
    print_board(board)

    while True:
        player_checker = players[current_player_idx]

        col_idx = get_valid_input(player_checker, cols, board)

        # If col_idx is None, player lost turn, skip placing
        if col_idx is not None:
            placed_row, placed_col = place_checker(board, col_idx, player_checker)
            clear_screen()
            print_board(board)

            # Check win
            if check_win(board, player_checker, placed_row, placed_col):
                print(f"Player {player_checker} won!")
                break

            # Check draw
            if check_draw(board):
                print("Game is a draw!")
                break
        else:
            # Column full, lose turn, just clear and print board again
            clear_screen()
            print_board(board)

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players


if __name__ == "__main__":
    main()
