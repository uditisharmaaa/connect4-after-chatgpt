import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  "
    for c in range(COLUMNS):
        header += "  " + chr(ord('A') + c) + " "
    print(header)
    # Print the board rows
    for r in range(ROWS):
        print("+---" * COLUMNS + "+")
        row_str = "|"
        for c in range(COLUMNS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+---" * COLUMNS + "+")

def is_valid_column(input_str):
    if len(input_str) != 1:
        return False
    c = input_str[0]
    if c < 'A' or c >= chr(ord('A') + COLUMNS):
        return False
    return True

def get_column_index(input_str):
    return ord(input_str) - ord('A')

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1

def place_checker(board, row, col, checker):
    board[row][col] = checker

def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if (board[r][c] == checker and board[r][c+1] == checker and
                board[r][c+2] == checker and board[r][c+3] == checker):
                return True
    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if (board[r][c] == checker and board[r+1][c] == checker and
                board[r+2][c] == checker and board[r+3][c] == checker):
                return True
    # Diagonal (down-right) check
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if (board[r][c] == checker and board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and board[r+3][c+3] == checker):
                return True
    # Diagonal (down-left) check
    for r in range(ROWS - 3):
        for c in range(3, COLUMNS):
            if (board[r][c] == checker and board[r+1][c-1] == checker and
                board[r+2][c-2] == checker and board[r+3][c-3] == checker):
                return True
    return False

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    num_players = MAX_PLAYERS
    players = CHECKERS[:num_players]

    # Random first player
    current_player_idx = random.randint(0, num_players - 1)

    # Print initial board
    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")
        user_input = input().strip().upper()

        if not is_valid_column(user_input):
            # Invalid input - must ask again
            continue

        col = get_column_index(user_input)
        row = get_next_open_row(board, col)

        if row == -1:
            # Column full: lose turn
            current_player_idx = (current_player_idx + 1) % num_players
            print_board(board)
            continue

        place_checker(board, row, col, current_checker)
        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if is_draw(board):
            print("Game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
