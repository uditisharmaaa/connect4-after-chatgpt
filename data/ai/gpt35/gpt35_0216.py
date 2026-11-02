import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4

PLAYERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    columns = len(board[0])
    # Print column headers
    header = "  "
    for i in range(columns):
        header += f"  {chr(ord('A') + i)} "
    print(header)
    # Print top line
    print("+" + "---+" * columns)
    for row in board:
        line = "|"
        for cell in row:
            line += f" {cell} |"
        print(line)
        print("+" + "---+" * columns)


def get_valid_column_input(player_checker, board):
    columns = len(board[0])
    valid_letters = [chr(ord('A') + i) for i in range(columns)]
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            # Invalid length
            continue
        if inp not in valid_letters:
            # Not in board columns
            continue
        col = ord(inp) - ord('A')
        # Check if column is full
        if board[0][col] != " ":
            # Column full, turn lost
            return None
        return col


def place_checker(board, col, checker):
    # Place checker in the lowest available row in the given column
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full, should not reach here if validation done properly
    return None, None


def check_win_from_position(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(r_step, c_step):
        count = 0
        r, c = row + r_step, col + c_step
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += r_step
            c += c_step
        return count

    # Directions: horizontal, vertical, diagonal1 (/), diagonal2 (\)
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # count current cell
        count += count_direction(dr, dc)
        count += count_direction(-dr, -dc)
        if count >= WIN_LENGTH:
            return True
    return False


def board_full(board):
    return all(cell != " " for cell in board[0])


def main():
    # Initialization
    rows, columns = ROWS, COLUMNS
    num_players = 2  # Submission requires 2 players enabled
    players = PLAYERS[:num_players]

    board = create_board(rows, columns)
    # Randomly pick starting player index
    current_player_idx = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]

        col = get_valid_column_input(current_checker, board)
        if col is None:
            # Column full, player loses turn
            current_player_idx = (current_player_idx + 1) % num_players
            continue

        row, col_placed = place_checker(board, col, current_checker)

        # Check win
        if check_win_from_position(board, row, col_placed, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw.")
            break

        current_player_idx = (current_player_idx + 1) % num_players


if __name__ == "__main__":
    main()
