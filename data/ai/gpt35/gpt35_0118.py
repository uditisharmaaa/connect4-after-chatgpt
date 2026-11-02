import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # support up to 5 players
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    labels = "  "
    for c in range(COLS):
        labels += chr(ord('A') + c) + "   "
    print(labels)

    # Print the board with horizontal separator lines
    line_sep = "+" + "---+" * COLS
    for r in range(ROWS):
        print(line_sep)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line_sep)

def input_to_col(user_input):
    if len(user_input) != 1:
        return -1
    letter = user_input.upper()
    if letter < 'A' or letter >= chr(ord('A') + COLS):
        return -1
    return ord(letter) - ord('A')

def place_checker(board, col, checker):
    # Start from bottom row going up, place checker in the first empty cell
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # column full

def check_win(board, row, col, checker):
    # Directions to check: horizontal, vertical,
    # diagonal down-right, diagonal down-left
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS -1)

    print_board(board)

    while True:
        checker = players[current_player_idx]
        print(f"Player {checker}, please enter a column:")
        user_input = input().strip()
        col = input_to_col(user_input)

        if col == -1:
            # Invalid input - re-ask without losing turn
            continue

        row = place_checker(board, col, checker)
        if row == -1:
            # Column full - turn lost
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
