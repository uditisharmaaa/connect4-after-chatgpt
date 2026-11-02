import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Support up to 5 players
WIN_CONDITION = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    # Column labels
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    for row in board:
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))

def is_valid_column(column_letter, columns):
    if len(column_letter) != 1:
        return False
    column_letter = column_letter.upper()
    if column_letter < 'A' or column_letter >= chr(ord('A') + columns):
        return False
    return True

def get_column_index(column_letter):
    return ord(column_letter.upper()) - ord('A')

def place_checker(board, column_idx, checker):
    """
    Place checker in the given column (lowest available spot).
    Return True if placed, False if column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][column_idx] == " ":
            board[row][column_idx] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    length = WIN_CONDITION

    # Check horizontal
    for r in range(rows):
        for c in range(cols - length + 1):
            if all(board[r][c + i] == checker for i in range(length)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - length + 1):
            if all(board[r + i][c] == checker for i in range(length)):
                return True

    # Check diagonal down-right
    for r in range(rows - length + 1):
        for c in range(cols - length + 1):
            if all(board[r + i][c + i] == checker for i in range(length)):
                return True

    # Check diagonal up-right
    for r in range(length - 1, rows):
        for c in range(cols - length + 1):
            if all(board[r - i][c + i] == checker for i in range(length)):
                return True

    return False

def check_draw(board):
    # If any cell in top row is empty, the board is not full
    return all(cell != " " for cell in board[0])

def get_player_input(player_checker, columns):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(user_input, columns):
            # Invalid column character
            continue
        col_idx = get_column_index(user_input)
        return col_idx

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]

        col_idx = get_player_input(current_checker, COLUMNS)

        placed = place_checker(board, col_idx, current_checker)
        if not placed:
            # Column full: turn lost (skip to next player)
            current_player_idx = (current_player_idx + 1) % PLAYERS
            continue

        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS


if __name__ == "__main__":
    main()
