import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers A, B, C, ...
    headers = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(headers))
    row_line = "+" + "---+" * len(board[0])
    for row in board:
        print(row_line)
        print("| " + " | ".join(row) + " |")
    print(row_line)

def get_player_input(player, board_cols):
    while True:
        choice = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(choice) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        col = ord(choice) - ord('A')
        if not (0 <= col < board_cols):
            print("Column out of range. Please enter a valid column letter.")
            continue
        return col

def place_checker(board, col, checker):
    # Place checker in lowest available spot in the column
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full, lose turn
    return None, None

def check_win(board, checker, row, col):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # count the placed checker itself
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLS)

    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    players_checkers = CHECKERS[:NUM_PLAYERS]

    print_board(board)

    while True:
        current_checker = players_checkers[current_player_index]
        col = get_player_input(current_checker, COLS)
        row, placed_col = place_checker(board, col, current_checker)

        if row is None:
            # Column full, lose turn
            print(f"Column {chr(ord('A') + col)} is full. Player {current_checker} loses this turn.")
        else:
            print_board(board)
            if check_win(board, current_checker, row, placed_col):
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print("Game is a draw!")
                break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
