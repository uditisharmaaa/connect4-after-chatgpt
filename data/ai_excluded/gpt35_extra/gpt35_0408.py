import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Extendable up to 5 players
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column headers A..Z (up to 26)
    headers = [chr(ord('A') + i) for i in range(columns)]
    print("  " + "   ".join(headers))
    print("+---" * columns + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * columns + "+")

def get_player_input(player_checker, columns, board):
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        if not col_input.isalpha() or not col_input.isupper():
            print("Invalid input. Please enter an uppercase letter (A-G).")
            continue
        col_index = ord(col_input) - ord('A')
        if col_index < 0 or col_index >= columns:
            print("Invalid column. Please enter a letter within the board's columns.")
            continue
        # Check if column is full
        if board[0][col_index] != " ":
            # According to assignment player loses turn if column full
            return None
        return col_index

def place_checker(board, col_index, checker):
    # place checker from bottom up
    for row in reversed(range(len(board))):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    # If here, column is full (shouldn't happen if checked before)
    return None

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Diagonal check (top-left to bottom-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal check (bottom-left to top-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def check_draw(board):
    # If any top row cell is empty, not draw yet
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current_player_idx]
        col = get_player_input(checker, COLUMNS, board)
        if col is None:
            # Column full, player loses turn, go to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        place_checker(board, col, checker)
        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
