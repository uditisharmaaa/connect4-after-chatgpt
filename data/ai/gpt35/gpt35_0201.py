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
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    cols = len(board[0])
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(labels))
    # Print rows with separators
    for row in board:
        print("+" + "---+" * cols)
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * cols)

def is_valid_column(col_letter, cols):
    if len(col_letter) != 1:
        return False
    col = ord(col_letter) - ord('A')
    if 0 <= col < cols:
        return True
    return False

def get_column_index(col_letter):
    return ord(col_letter) - ord('A')

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place checker in lowest available row in column
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None

def check_win(board, row, col, checker):
    # Check horizontal
    count = 0
    for c in range(len(board[0])):
        if board[row][c] == checker:
            count += 1
            if count >= WIN_COUNT:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(len(board)):
        if board[r][col] == checker:
            count += 1
            if count >= WIN_COUNT:
                return True
        else:
            count = 0

    # Check diagonal /
    count = 0
    start_row = row
    start_col = col
    # Move up-right as far as possible
    while start_row > 0 and start_col < len(board[0]) -1:
        start_row -= 1
        start_col += 1
    r, c = start_row, start_col
    while r < len(board) and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count >= WIN_COUNT:
                return True
        else:
            count = 0
        r += 1
        c -= 1

    # Check diagonal \
    count = 0
    start_row = row
    start_col = col
    # Move up-left as far as possible
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    r, c = start_row, start_col
    while r < len(board) and c < len(board[0]):
        if board[r][c] == checker:
            count += 1
            if count >= WIN_COUNT:
                return True
        else:
            count = 0
        r += 1
        c += 1

    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS -1)
    clear_screen()
    print_board(board)

    while True:
        checker = players[current_player_index]
        print(f"Player {checker}, please enter a column:")
        user_input = input().strip().upper()
        # Validate input
        if not is_valid_column(user_input, COLS):
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = get_column_index(user_input)
        if is_column_full(board, col):
            # Player loses turn if column full
            print(f"Column {user_input} is full. You lose your turn.")
            # Switch player
            current_player_index = (current_player_index +1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue
        pos = place_checker(board, col, checker)
        clear_screen()
        print_board(board)
        if check_win(board, pos[0], pos[1], checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break
        current_player_index = (current_player_index +1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
