import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4
PLAYERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    separator = "+" + "---+" * cols
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def get_valid_column_input(players_cols):
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1:
            # Only single letters allowed
            continue
        if col_input not in players_cols:
            # Not a valid column letter
            continue
        return col_input

def find_row_to_place(board, col_index):
    for row in reversed(range(len(board))):
        if board[row][col_index] == " ":
            return row
    return None  # Column full

def check_four_in_a_row(line):
    count = 0
    last = None
    for cell in line:
        if cell != " " and cell == last:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 1
            last = cell
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Check diagonal (\ direction)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[r+i][c+i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    # Check diagonal (/ direction)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[r - i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    # Settings as per submission requirements
    rows = ROWS
    cols = COLUMNS
    num_players = 2
    checkers = PLAYERS[:num_players]
    board = create_board(rows, cols)

    players_cols = string.ascii_uppercase[:cols]

    # Random first player
    current_player_idx = random.randint(0, num_players - 1)

    print_board(board)
    print(f"Player {checkers[current_player_idx]}, you start first.")

    while True:
        player = checkers[current_player_idx]
        print_board(board)
        print(f"Player {player}, please enter a column:")

        col_letter = get_valid_column_input(players_cols)
        col_index = players_cols.index(col_letter)

        row_index = find_row_to_place(board, col_index)
        if row_index is None:
            # Column full: turn lost
            # According to assignment: turn invalid, player loses the turn
            current_player_idx = (current_player_idx + 1) % num_players
            continue

        # Place checker
        board[row_index][col_index] = player

        # Check win
        if check_win(board, player):
            print_board(board)
            print(f"Player {player} won!")
            break

        # Check draw
        if board_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Next player turn
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
