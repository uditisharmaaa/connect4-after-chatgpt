import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    # Print the board rows and separators
    for r in range(len(board)):
        print("+" + "---+" * len(board[0]))
        row_str = "|"
        for c in range(len(board[0])):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * len(board[0]))

def is_valid_column(col_letter, cols):
    if len(col_letter) != 1 or not ('A' <= col_letter <= chr(ord('A') + cols - 1)):
        return False
    return True

def get_column_index(col_letter):
    return ord(col_letter) - ord('A')

def place_checker(board, col, checker):
    # Place checker in the lowest available row in the column
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full
    return None

def check_winner(board, row, col, checker):
    # Directions: horizontal, vertical, diag /
    directions = [
        (0, 1),   # horiz right
        (1, 0),   # vertical down
        (1, 1),   # diag down-right
        (1, -1)   # diag down-left
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
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:MAX_PLAYERS]  # select checkers for enabled players
    current_player_idx = random.randint(0, MAX_PLAYERS - 1)
    print_board(board)

    while True:
        checker = players[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        # Input loop until valid input or full column
        while True:
            col_letter = input(prompt).strip().upper()
            if not is_valid_column(col_letter, COLUMNS):
                print("Invalid column. Please enter a letter from A to " + chr(ord('A') + COLUMNS - 1) + ".")
                continue
            col_idx = get_column_index(col_letter)
            placed = place_checker(board, col_idx, checker)
            if placed is None:
                # Column full, turn lost
                print("Column full, turn lost.")
                break
            else:
                row_placed, col_placed = placed
                break

        print_board(board)

        # If checker placed, check for win
        if placed is not None:
            if check_winner(board, row_placed, col_placed, checker):
                print(f"Player {checker} won!")
                break
        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player turn
        current_player_idx = (current_player_idx + 1) % MAX_PLAYERS

if __name__ == "__main__":
    main()
