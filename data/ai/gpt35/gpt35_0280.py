import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column headers
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(header)
    # Print each row
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")


def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    col_index = ord(col_char) - ord('A')
    if 0 <= col_index < cols:
        return True
    return False


def get_column_index(col_char):
    return ord(col_char) - ord('A')


def place_checker(board, col_index, checker):
    # Place checker in the lowest empty cell in column col_index
    for row_i in reversed(range(len(board))):
        if board[row_i][col_index] == " ":
            board[row_i][col_index] = checker
            return True
    return False  # Column is full


def is_winning_move(board, r, c, checker):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check forward direction
        rr, cc = r + dr, c + dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc
        # Check backward direction
        rr, cc = r - dr, c - dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr -= dr
            cc -= dc
        if count >= 4:
            return True
    return False


def check_for_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == checker:
                if is_winning_move(board, r, c, checker):
                    return True
    return False


def is_draw(board):
    for row in board:
        if " " in row:
            return False
    return True


def find_checker_row(board, col_index):
    for row_i in range(len(board)):
        if board[row_i][col_index] != " ":
            return row_i
    return len(board)


def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "
        col_char = input(prompt).strip().upper()

        # Validate input
        while not is_valid_column(col_char, COLS):
            col_char = input(f"Invalid column. {prompt}").strip().upper()

        col_index = get_column_index(col_char)

        # Check if column is full
        if not place_checker(board, col_index, current_checker):
            # Turn lost
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Find row where checker was placed
        placed_row = None
        for r in range(ROWS):
            if board[r][col_index] == current_checker:
                placed_row = r
                break
        # Check for win
        if check_for_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if is_draw(board):
            print("Game is a draw!")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % PLAYERS


if __name__ == "__main__":
    main()
