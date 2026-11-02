import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([" "] * COLUMNS)
    return board

def print_board(board):
    clear_screen()
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(letters))
    # Print board rows
    for row in board:
        print("+" + "---+" * COLUMNS)
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * COLUMNS)

def is_valid_column(col):
    if len(col) != 1:
        return False
    if not ('A' <= col <= chr(ord('A') + COLUMNS - 1)):
        return False
    return True

def column_to_index(col):
    return ord(col) - ord('A')

def get_next_open_row(board, col_idx):
    # Returns the index of the lowest empty row in the column.
    # Rows start from top at index 0 (top row).
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return None  # Column full

def place_checker(board, row, col_idx, checker):
    board[row][col_idx] = checker

def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True
    # Diagonal (down-right)
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    # Diagonal (down-left)
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[r + i][c - i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_draw(board):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        print(f"Player {player_checker}, please enter a column:")

        valid_input = False
        while not valid_input:
            col = input().strip().upper()
            if not is_valid_column(col):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col_idx = column_to_index(col)
            open_row = get_next_open_row(board, col_idx)
            if open_row is None:
                # If column full, lose the turn
                print(f"Column {col} is full, you lose your turn.")
                valid_input = True  # End input loop for turn
                break
            else:
                place_checker(board, open_row, col_idx, player_checker)
                valid_input = True

        print_board(board)

        if open_row is not None:
            if check_win(board, player_checker):
                print(f"Player {player_checker} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break

        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
