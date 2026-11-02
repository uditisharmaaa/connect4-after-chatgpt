import os
import random
import sys

# Constants (you may change these for testing; submission should be 6x7 and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Ensure constraints
COLS = max(1, min(COLS, 26))
NUM_PLAYERS = max(2, min(NUM_PLAYERS, 5))
PLAYERS = CHECKERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Header letters
    header = "  " + "   ".join([chr(ord('A') + c) for c in range(cols)])
    print(header)
    # Top border
    print("+" + ("---+" * cols))
    for r in range(len(board)):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + ("---+" * cols))

def get_valid_column_input(cols):
    while True:
        user_in = input().strip().upper()
        if len(user_in) != 1 or not user_in.isalpha():
            print("Invalid input. Please enter a single letter for the column:")
            continue
        col = ord(user_in) - ord('A')
        if 0 <= col < cols:
            return col, user_in
        else:
            print("Column out of range. Please enter a valid column letter:")

def drop_checker(board, col, checker):
    # Place checker in the lowest available row in the given column.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1  # Column full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and board[r][c+1] == checker and
                board[r][c+2] == checker and board[r][c+3] == checker):
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - 3):
            if (board[r][c] == checker and board[r+1][c] == checker and
                board[r+2][c] == checker and board[r+3][c] == checker):
                return True

    # Diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == checker and board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and board[r+3][c+3] == checker):
                return True

    # Diagonal down-left
    for r in range(rows - 3):
        for c in range(3, cols):
            if (board[r][c] == checker and board[r+1][c-1] == checker and
                board[r+2][c-2] == checker and board[r+3][c-3] == checker):
                return True

    return False

def check_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        checker = PLAYERS[current_player]
        print(f"Player {checker}, please enter a column:")
        col_index, col_letter = get_valid_column_input(COLS)

        # Attempt to drop checker
        row_placed = drop_checker(board, col_index, checker)
        if row_placed == -1:
            # Column full, player loses turn
            print(f"Column {col_letter} is full. Turn lost.")
            # Check draw before switching (board unchanged though)
            if check_draw(board):
                clear_screen()
                print_board(board)
                print("It's a draw!")
                break
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS
        else:
            # Successful move
            if check_win(board, checker):
                clear_screen()
                print_board(board)
                print(f"Player {checker} won!")
                break
            if check_draw(board):
                clear_screen()
                print_board(board)
                print("It's a draw!")
                break
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS

        # Print updated board for next turn
        clear_screen()
        print_board(board)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
