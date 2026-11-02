import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    for row in range(len(board)):
        print("+---" * len(board[0]) + "+")
        print("| " + " | ".join(board[row]) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_column(letter):
    return letter in COLUMN_LABELS

def column_to_index(letter):
    return ord(letter) - ord('A')

def place_checker(board, column_idx, checker):
    # Start from bottom row, find first empty cell
    for row in reversed(range(len(board))):
        if board[row][column_idx] == " ":
            board[row][column_idx] = checker
            return row
    return -1  # Column full

def check_win(board, row, col, checker):
    return (
        check_direction(board, row, col, checker, 0, 1) or  # Horizontal
        check_direction(board, row, col, checker, 1, 0) or  # Vertical
        check_direction(board, row, col, checker, 1, 1) or  # Diagonal down-right
        check_direction(board, row, col, checker, 1, -1)    # Diagonal down-left
    )

def check_direction(board, row, col, checker, delta_row, delta_col):
    count = 1  # Count the placed checker itself

    # Check one direction
    r, c = row + delta_row, col + delta_col
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col

    # Check opposite direction
    r, c = row - delta_row, col - delta_col
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
        count += 1
        r -= delta_row
        c -= delta_col

    return count >= WIN_COUNT

def board_full(board):
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True

def get_valid_input(current_player):
    while True:
        inp = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            continue
        if not is_valid_column(inp):
            continue
        return inp

def main():
    random.seed()  # Init random

    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        checker = players[current_player_idx]
        col_letter = get_valid_input(checker)
        col_idx = column_to_index(col_letter)

        placed_row = place_checker(board, col_idx, checker)
        if placed_row == -1:
            # Column full, player loses turn
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, placed_row, col_idx, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("Game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
