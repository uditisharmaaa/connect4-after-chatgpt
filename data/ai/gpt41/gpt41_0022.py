import os
import random
import string

# --------- CONSTANTS ---------
ROWS = 6           # Number of rows (default: 6)
COLUMNS = 7        # Number of columns (default: 7)
MAX_COLUMNS = 26   # Max columns, because letters A-Z
NUM_PLAYERS = 2    # Number of players (between 2 and 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']
EMPTY = " "


def clear_screen():
    os.system('clear')  # On Linux/Unix
    # os.system('cls')  # For Windows, if needed


def create_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Print column headers (A, B, C, ...)
    col_labels = "  ".join(string.ascii_uppercase[:len(board[0])])
    print("  " + "   ".join(string.ascii_uppercase[:len(board[0])]))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))


def get_valid_input(board):
    valid_cols = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    while True:
        user_input = input().strip().upper()
        if len(user_input) != 1:
            print("Invalid input: enter a single letter for the column (A-{})".format(valid_cols[-1]))
            continue
        if user_input not in valid_cols:
            print("Invalid input: enter a letter for a column (A-{})".format(valid_cols[-1]))
            continue
        col_idx = valid_cols.index(user_input)
        # Check if the column is full
        if board[0][col_idx] != EMPTY:
            print("Column is full! You lose your turn.")
            return None  # Lose the turn
        return col_idx


def place_checker(board, col, checker):
    # Place the checker in the lowest available row in that column
    for i in reversed(range(len(board))):
        if board[i][col] == EMPTY:
            board[i][col] = checker
            return i, col  # Return the row and column where placed
    return None, None  # Should not happen (we check for full in input)


def check_win(board, row, col, checker):
    # Check all directions for 4 in a row

    def count_dir(delta_row, delta_col):
        r, c = row, col
        count = 0
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col
        return count - 1  # subtract the starting point (to avoid double count)

    directions = [ (0,1), (1,0), (1,1), (1,-1) ]  # horiz, vert, diag (/), diag (\)
    for dr, dc in directions:
        count = 1  # start with the checker just placed
        count += count_dir(dr, dc)
        count += count_dir(-dr, -dc)
        if count >= 4:
            return True
    return False


def check_draw(board):
    for cell in board[0]:
        if cell == EMPTY:
            return False
    return True


def main():
    # Set up game
    # For grading, these should be 6x7 and 2 players
    rows = ROWS
    cols = COLUMNS
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]

    board = create_board(rows, cols)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)
    print("Player {}, please enter a column:".format(players[current_player]))

    while True:
        col = get_valid_input(board)
        # If column is full (input returns None), skip this players turn
        if col is None:
            current_player = (current_player + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            print("Player {}, please enter a column:".format(players[current_player]))
            continue

        row, column = place_checker(board, col, players[current_player])

        clear_screen()
        print_board(board)

        # Check for a win
        if check_win(board, row, column, players[current_player]):
            print("Player {} won!".format(players[current_player]))
            break

        # Check for a draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS
        print("Player {}, please enter a column:".format(players[current_player]))


if __name__ == '__main__':
    main()
