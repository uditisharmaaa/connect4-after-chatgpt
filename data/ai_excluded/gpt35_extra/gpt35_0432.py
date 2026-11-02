import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
WIN_COUNT = 4
PLAYERS = ["X", "O", "V", "H", "M"]  # Max 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    cols_label = "  "
    for c in range(len(board[0])):
        cols_label += f"  {chr(ord('A') + c)} "
    print(cols_label)
    # Print board with separators consistent with example
    hr_line = "+" + "---+" * len(board[0])
    for r in range(len(board)):
        print(hr_line)
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(hr_line)

def is_valid_column(col_letter, cols):
    if len(col_letter) != 1:
        return False
    if not ('A' <= col_letter <= chr(ord('A') + cols - 1)):
        return False
    return True

def get_column_index(col_letter):
    return ord(col_letter) - ord('A')

def place_checker(board, col, checker):
    """
    Place checker into the lowest empty spot in the column.
    If column full, return False.
    Else return True.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # column full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Diagonal checks (top-left to bottom-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal checks (bottom-left to top-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        current_checker = players[current_player_idx]
        while True:
            inp = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            if not is_valid_column(inp, COLUMNS):
                continue  # invalid input, ask again
            col_idx = get_column_index(inp)
            if not place_checker(board, col_idx, current_checker):
                # column full -> lose turn
                break
            else:
                # checker placed, break input loop
                break

        # Check win or draw only if checker placed; if not placed (column full), next player's turn
        if board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
