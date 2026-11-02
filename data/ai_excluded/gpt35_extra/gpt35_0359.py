import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
WIN_CONDITION = 4

# Using exactly 2 players as per submission requirement
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    # Print the board with row separators
    for r in range(len(board)):
        print("+" + "---+" * len(board[0]))
        print("|" + "|".join(f" {board[r][c]} " for c in range(len(board[0]))) + "|")
    print("+" + "---+" * len(board[0]))


def is_valid_column(col_input, board):
    if len(col_input) != 1:
        return False
    if not col_input.isalpha() or not col_input.isupper():
        return False
    col_index = ord(col_input) - ord('A')
    if col_index < 0 or col_index >= len(board[0]):
        return False
    return True


def column_has_space(board, col_index):
    # Check if top row in column is free -> means column has space
    return board[0][col_index] == " "


def place_checker(board, col_index, checker):
    # Start from bottom row and go up to place checker in the lowest empty space
    for row in reversed(range(len(board))):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    # Column full - player loses turn, indicate by returning None
    return None


def check_win(board, checker, last_row, last_col):
    # Directions: horizontal, vertical, diag1(/), diag2(\)
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
        # Check forward direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check backward direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_CONDITION:
            return True
    return False


def board_full(board):
    # If no spaces in top row, board is full
    return all(cell != " " for cell in board[0])


def next_player_index(current_index):
    return (current_index + 1) % NUM_PLAYERS


def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    while True:
        checker = PLAYER_CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")

        # Validate input for column
        while True:
            user_input = input().strip()
            if not is_valid_column(user_input, board):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col_index = ord(user_input) - ord('A')
            if not column_has_space(board, col_index):
                # Column full, player loses turn immediately
                print(f"Column {user_input} is full. You lose your turn.")
                break
            # Valid input & space available
            placement_pos = place_checker(board, col_index, checker)
            if placement_pos is not None:
                last_row, last_col = placement_pos
                break
            else:
                # Should not happen due to column_has_space check
                print(f"Column {user_input} is full. You lose your turn.")
                break

        print_board(board)

        # If placement was successful, check win/draw
        if placement_pos is not None:
            if check_win(board, checker, last_row, last_col):
                print(f"Player {checker} won!")
                break
            if board_full(board):
                print("The game is a draw!")
                break

        # Switch to next player
        current_player = next_player_index(current_player)


if __name__ == "__main__":
    main()
