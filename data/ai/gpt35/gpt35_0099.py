import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # up to 5 players

WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers A, B, C, ...
    headers = "  " + "   ".join(chr(ord("A") + i) for i in range(len(board[0])))
    print(headers)
    # Print rows with separators
    row_separator = "+" + "---+" * len(board[0])
    for row in board:
        print(row_separator)
        print("| " + " | ".join(row) + " |")
    print(row_separator)

def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    if not ('A' <= col_char <= chr(ord('A') + cols - 1)):
        return False
    return True

def get_column_index(col_char):
    return ord(col_char) - ord('A')

def column_full(board, col_idx):
    # If top row is not empty, column is full
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    # Place checker in lowest available row in column col_idx
    for row_idx in range(len(board)-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    # No space found
    return None

def check_win(board, row, col, checker):
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1
        # Check forward
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players_checkers = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        checker = players_checkers[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        col_char = input(prompt).strip().upper()

        # Validate input
        if not is_valid_column(col_char, COLUMNS):
            # Invalid column letter
            continue

        col_idx = get_column_index(col_char)

        if column_full(board, col_idx):
            # Column full, player loses turn
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        pos = place_checker(board, col_idx, checker)
        if pos is None:
            # Should not happen as we checked column_full
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        row, col = pos
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("The game is a draw.")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
