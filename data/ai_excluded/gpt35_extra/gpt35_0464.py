import os
import random
import string

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    headers = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(headers)
    line = "+" + ("---+" * cols)
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def is_valid_column(col_char, board):
    cols = len(board[0])
    if len(col_char) != 1 or col_char not in string.ascii_uppercase[:cols]:
        return False
    col_index = ord(col_char) - ord('A')
    # Check if the column is full
    if board[0][col_index] != " ":
        return False
    return True

def place_checker(board, col_char, checker):
    col_index = ord(col_char) - ord('A')
    # Start from bottom row, place checker in lowest empty cell in the column
    for row_index in range(len(board)-1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return (row_index, col_index)  # Return position where placed
    # If column is full, return None (shouldn't get here if validated)
    return None

def check_win(board, checker, last_row, last_col):
    rows = len(board)
    cols = len(board[0])

    def count_direction(delta_r, delta_c):
        count = 0
        r, c = last_row + delta_r, last_col + delta_c
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += delta_r
            c += delta_c
        return count

    # Check horizontal (left + right)
    hor_count = 1 + count_direction(0, -1) + count_direction(0, 1)
    if hor_count >= WIN_LENGTH:
        return True

    # Check vertical (up + down)
    ver_count = 1 + count_direction(-1, 0) + count_direction(1, 0)
    if ver_count >= WIN_LENGTH:
        return True

    # Check diagonal /
    diag1_count = 1 + count_direction(-1, 1) + count_direction(1, -1)
    if diag1_count >= WIN_LENGTH:
        return True

    # Check diagonal \
    diag2_count = 1 + count_direction(-1, -1) + count_direction(1, 1)
    if diag2_count >= WIN_LENGTH:
        return True

    return False

def board_full(board):
    # Board is full if top row has no empty cells
    return all(cell != " " for cell in board[0])

def get_next_player(current_index, total_players):
    return (current_index + 1) % total_players

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        while True:
            user_input = input().strip().upper()
            if not user_input or len(user_input) != 1:
                print("Invalid input. Enter a single column letter (A-G):")
                continue
            if not (user_input in string.ascii_uppercase[:NUM_COLS]):
                print(f"Column out of range. Enter a column letter between A and {chr(ord('A') + NUM_COLS - 1)}:")
                continue
            # If column is full, player loses turn (print message, break input loop)
            col_index = ord(user_input) - ord('A')
            if board[0][col_index] != " ":
                print("Column is full, you lose your turn.")
                break
            else:
                # valid input and column not full
                break

        # If column was full, skip placing and go to next player
        if board[0][col_index] == " ":
            placed_pos = place_checker(board, user_input, current_checker)
            if placed_pos is None:
                # Should not happen due to validation
                print("Unexpected error placing checker.")
                continue

            # Check for win
            if check_win(board, current_checker, placed_pos[0], placed_pos[1]):
                print_board(board)
                print(f"Player {current_checker} won!")
                break

            # Check for draw
            if board_full(board):
                print_board(board)
                print("Game draw! The board is full.")
                break

        # Move to next player
        current_player_idx = get_next_player(current_player_idx, NUM_PLAYERS)

if __name__ == "__main__":
    main()
