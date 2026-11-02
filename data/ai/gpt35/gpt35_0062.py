import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_CONDITION = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board


def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print top border
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)


def is_valid_column(col):
    return col in COLUMN_LABELS


def column_full(board, col_idx):
    # If top cell is not empty, column is full
    return board[0][col_idx] != " "


def get_next_open_row(board, col_idx):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return None  # Column full


def place_checker(board, row, col_idx, checker):
    board[row][col_idx] = checker


def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLUMNS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_CONDITION:
                    return True
            else:
                count = 0
    # Check vertical
    for c in range(COLUMNS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_CONDITION:
                    return True
            else:
                count = 0
    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - WIN_CONDITION + 1):
        for c in range(COLUMNS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True
    # Check diagonal (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, ROWS):
        for c in range(COLUMNS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True
    return False


def board_full(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True


def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        while True:
            choice = input().strip().upper()
            if len(choice) != 1:
                print("Invalid input. Please enter a single column letter:")
                continue
            if not is_valid_column(choice):
                print("Invalid column letter. Please enter a valid column:")
                continue
            col_idx = COLUMN_LABELS.index(choice)
            if column_full(board, col_idx):
                # Player loses the turn if column full
                print(f"Column {choice} is full. You lose your turn.")
                break
            else:
                row_idx = get_next_open_row(board, col_idx)
                place_checker(board, row_idx, col_idx, current_checker)
                break

        print_board(board)

        if not column_full(board, col_idx):
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if board_full(board):
                print("The game is a draw!")
                break

        current_player_idx = (current_player_idx + 1) % PLAYERS


if __name__ == "__main__":
    main()
