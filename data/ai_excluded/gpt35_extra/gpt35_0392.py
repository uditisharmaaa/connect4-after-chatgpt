import os
import random

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    # Print board rows with border
    for r in range(len(board)):
        print("+" + "---+" * cols)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * cols)

def valid_column_input(input_str, cols):
    if len(input_str) != 1:
        return False
    c = input_str.upper()
    if not ('A' <= c <= chr(ord('A') + cols - 1)):
        return False
    return True

def col_to_index(col_char):
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    """
    Place checker in the specified column, bottom-most available spot.
    Returns:
        row index where checker was placed or
        -1 if column is full
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row
    return -1

def winner_check_line(line, checker):
    count = 0
    for c in line:
        if c == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        if winner_check_line(board[r], checker):
            return True

    # Check vertical
    for c in range(cols):
        col_line = [board[r][c] for r in range(rows)]
        if winner_check_line(col_line, checker):
            return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            diag = [board[r+i][c+i] for i in range(WIN_COUNT)]
            if all(cell == checker for cell in diag):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            diag = [board[r-i][c+i] for i in range(WIN_COUNT)]
            if all(cell == checker for cell in diag):
                return True

    return False

def board_full(board):
    return all(board[0][c] != " " for c in range(len(board[0])))

def main():
    rows = ROWS
    cols = COLS
    num_players = 2
    checkers = PLAYERS[:num_players]

    board = create_board(rows, cols)
    current_player_idx = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        checker = checkers[current_player_idx]
        # Prompt input
        while True:
            prompt = f"Player {checker}, please enter a column: "
            user_input = input(prompt).strip().upper()
            if not valid_column_input(user_input, cols):
                continue
            col_idx = col_to_index(user_input)
            placed_row = place_checker(board, col_idx, checker)
            if placed_row == -1:
                # Column full, player loses turn as per specs
                # So break input loop and continue game loop with next player
                break
            else:
                # successful placement
                print_board(board)

                if check_winner(board, checker):
                    print(f"Player {checker} won!")
                    return
                if board_full(board):
                    print("The game is a draw.")
                    return
                break  # exit input loop, move to next player

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
