import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Max 5 players, use first n for actual players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))

    # Print rows and horizontal dividers
    for r in range(len(board)):
        print("+" + "---+" * cols)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * cols)

def is_valid_column(inp, cols):
    if len(inp) != 1:
        return False
    c = inp.upper()
    return 'A' <= c < chr(ord('A') + cols)

def col_index(inp):
    return ord(inp.upper()) - ord('A')

def place_checker(board, col, checker):
    # Place checker in the lowest available row in column col
    # Return True if placed, False if column full
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    win_len = 4

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_len + 1):
            if all(board[r][c+i] == checker for i in range(win_len)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - win_len + 1):
            if all(board[r+i][c] == checker for i in range(win_len)):
                return True

    # Check diagonal down-right
    for r in range(rows - win_len + 1):
        for c in range(cols - win_len + 1):
            if all(board[r+i][c+i] == checker for i in range(win_len)):
                return True

    # Check diagonal up-right
    for r in range(win_len -1, rows):
        for c in range(cols - win_len + 1):
            if all(board[r-i][c+i] == checker for i in range(win_len)):
                return True

    return False

def board_full(board):
    # If any cell is empty, return False
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def get_player_input(current_player_checker, cols):
    while True:
        inp = input(f"Player {current_player_checker}, please enter a column: ").strip()
        if not is_valid_column(inp, cols):
            # Invalid length or character out of range
            continue
        return inp.upper()

def main():
    board = create_board(ROWS, COLS)
    active_players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        player_checker = active_players[current_player_index]

        inp = get_player_input(player_checker, COLS)
        col = col_index(inp)

        placed = place_checker(board, col, player_checker)
        if not placed:
            # Column full, player loses turn (no retry)
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("Draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
