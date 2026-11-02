import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players, use first PLAYERS of these
WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]


def clear_screen():
    os.system('clear')


def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COLUMN_LABELS))
    # Print each row
    for r in range(ROWS):
        print("+" + "---+" * COLUMNS)
        row_str = "|"
        for c in range(COLUMNS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * COLUMNS)


def get_next_player(current):
    return (current + 1) % PLAYERS


def valid_column_input(col):
    if len(col) != 1:
        return False
    if col not in COLUMN_LABELS:
        return False
    return True


def column_full(board, col_index):
    return board[0][col_index] != " "  # If top row is occupied, column is full


def place_checker(board, col_index, checker):
    # Place checker at lowest empty spot in column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    return None, None  # Should not happen if checked for full before


def check_win(board, row, col, checker):
    # Check all directions from the placed checker
    # Directions: horizontal, vertical, two diagonals
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # count includes the placed checker itself

        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True
    return False


def board_full(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True


def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")

        # Input validation loop
        while True:
            user_input = input().strip().upper()
            if not valid_column_input(user_input):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col_index = COLUMN_LABELS.index(user_input)
            if column_full(board, col_index):
                # Column full, player loses turn
                print(f"Column {user_input} is full, turn lost.")
                break
            else:
                # Place the checker
                row_placed, col_placed = place_checker(board, col_index, checker)
                break

        print_board(board)

        # If we placed a checker, check for win and draw
        if not column_full(board, col_index):
            if check_win(board, row_placed, col_placed, checker):
                print(f"Player {checker} won!")
                break
            if board_full(board):
                print("The game is a draw!")
                break

        current_player = get_next_player(current_player)


if __name__ == "__main__":
    main()
