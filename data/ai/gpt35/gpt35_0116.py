import os
import random

# Constants - you can change these to test different dimensions or players
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    # Print column labels
    columns = len(board[0])
    col_labels = [chr(ord('A') + i) for i in range(columns)]
    print("  " + "   ".join(col_labels))
    # Print board grid
    for r in range(len(board)):
        print("+" + "---+" * columns)
        row_str = "|"
        for c in range(columns):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * columns)


def is_valid_column_input(inp, columns):
    if len(inp) != 1:
        return False
    if not ('A' <= inp <= chr(ord('A') + columns - 1)):
        return False
    return True


def get_column_index(inp):
    return ord(inp) - ord('A')


def get_lowest_empty_row(board, col):
    # From bottom row up, find first empty slot
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1  # column full


def place_checker(board, col, checker):
    row = get_lowest_empty_row(board, col)
    if row == -1:
        return False
    board[row][col] = checker
    return True


def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + offset] == checker for offset in range(WIN_LENGTH)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + offset][c] == checker for offset in range(WIN_LENGTH)):
                return True

    # Diagonal (down-right) check
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + offset][c + offset] == checker for offset in range(WIN_LENGTH)):
                return True

    # Diagonal (up-right) check
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - offset][c + offset] == checker for offset in range(WIN_LENGTH)):
                return True

    return False


def board_full(board):
    return all(cell != " " for row in board for cell in row)


def get_player_input(player_checker, columns):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column_input(inp, columns):
            continue
        col = get_column_index(inp)
        yield col


def main():
    # Setup
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]

    current_player_index = random.randint(0, PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)

        player = players[current_player_index]

        # Input phase
        valid_move = False
        while not valid_move:
            col_input_iter = get_player_input(player, COLUMNS)
            col = next(col_input_iter)
            # Try to place checker
            if place_checker(board, col, player):
                valid_move = True
            else:
                # Column full, player loses turn
                # According to instructions, no re-entry for full column
                # Just break to next player
                valid_move = False
                break

        # After move, check for winner or draw ONLY if a move was made
        if valid_move:
            if check_winner(board, player):
                clear_screen()
                print_board(board)
                print(f"Player {player} won!")
                break
            if board_full(board):
                clear_screen()
                print_board(board)
                print("The game is a draw.")
                break

        # Move to next player (if turn lost due to full column, still moves to next player)
        current_player_index = (current_player_index + 1) % PLAYERS


if __name__ == "__main__":
    main()
