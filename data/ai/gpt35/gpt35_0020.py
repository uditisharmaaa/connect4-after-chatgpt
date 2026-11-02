import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
COLUMN_LETTERS = [chr(ord("A") + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  " + "   ".join(COLUMN_LETTERS)
    print(header)
    # Print board with borders
    border = "+" + "---+" * COLUMNS
    for row in board:
        print(border)
        row_str = "|"
        for cell in row:
            row_str += f" {cell} |"
        print(row_str)
    print(border)

def choose_start_player(player_count):
    return random.randint(0, player_count - 1)

def input_column(player_checker):
    prompt = f"Player {player_checker}, please enter a column: "
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single uppercase letter (A-G).")
            continue
        if user_input not in COLUMN_LETTERS:
            print(f"Invalid column. Please enter a letter A-{COLUMN_LETTERS[-1]}.")
            continue
        return user_input

def place_checker(board, column_letter, checker):
    col_idx = ord(column_letter) - ord("A")
    # Find lowest empty row in column
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return True, row_idx, col_idx
    # Column full
    return False, None, None

def check_win(board, row, col, checker):
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def check_draw(board):
    # If any cell in top row is empty -> not full
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYER_COUNT]
    current_player_idx = choose_start_player(PLAYER_COUNT)
    print_board(board)

    while True:
        current_checker = players[current_player_idx]

        col_letter = input_column(current_checker)

        placed, r, c = place_checker(board, col_letter, current_checker)
        if not placed:
            # If column is full, player loses turn
            # So advance player and print board before next turn
            print_board(board)
            current_player_idx = (current_player_idx + 1) % PLAYER_COUNT
            continue

        print_board(board)

        # Check for win
        if check_win(board, r, c, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
