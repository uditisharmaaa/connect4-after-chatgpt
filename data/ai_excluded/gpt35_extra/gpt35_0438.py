import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

# Game settings for submission: 6 rows x 7 columns, 2 players
NUM_PLAYERS = 2
BOARD_ROWS = ROWS
BOARD_COLUMNS = COLUMNS
CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(labels))
    # Print board with separators
    for row in range(len(board)):
        print("+---" * cols + "+")
        row_str = ""
        for col in range(cols):
            row_str += "| " + board[row][col] + " "
        print(row_str + "|")
    print("+---" * cols + "+")


def is_valid_column_input(column_input, cols):
    # Must be single uppercase letter within board limits
    if len(column_input) != 1:
        return False
    if not ('A' <= column_input <= chr(ord('A') + cols - 1)):
        return False
    return True


def get_column_index(column_input):
    return ord(column_input) - ord('A')


def get_lowest_empty_row(board, col):
    # Returns the bottom-most empty row in the given column or -1 if full
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


def place_checker(board, col, checker):
    row_to_place = get_lowest_empty_row(board, col)
    if row_to_place == -1:
        return False  # Column full
    board[row_to_place][col] = checker
    return True


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for row in range(rows):
        count = 0
        for col in range(cols):
            if board[row][col] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check vertical
    for col in range(cols):
        count = 0
        for row in range(rows):
            if board[row][col] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_COUNT + 1):
        for col in range(cols - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[row + i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_COUNT - 1, rows):
        for col in range(cols - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[row - i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    return False


def check_draw(board):
    # Draw if no empty spaces in top row
    top_row = board[0]
    for cell in top_row:
        if cell == " ":
            return False
    return True


def main():
    board = create_board(BOARD_ROWS, BOARD_COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        valid_input = False

        while not valid_input:
            player_input = input(f"Player {current_checker}, please enter a column: ").strip()
            if player_input == "":
                continue
            player_input = player_input.upper()
            if not is_valid_column_input(player_input, BOARD_COLUMNS):
                continue
            col_index = get_column_index(player_input)
            # Check if column full - if full, turn lost
            if get_lowest_empty_row(board, col_index) == -1:
                # Turn lost for full column
                valid_input = True  # Move on even if placing checker failed
            else:
                # Place checker
                placed = place_checker(board, col_index, current_checker)
                if placed:
                    valid_input = True

        print_board(board)

        # If last move placed a checker (not turn lost for full column), check for win:
        if get_lowest_empty_row(board, col_index) != -1 or (get_lowest_empty_row(board, col_index) == -1):
            # Only check win if a checker was placed this turn
            if board == create_board(BOARD_ROWS, BOARD_COLUMNS):
                # Empty board - no moves placed - skip
                pass
            else:
                # Check for win only if a checker was placed (means column not full at input time)
                if board[get_lowest_empty_row(board, col_index)+1 if get_lowest_empty_row(board, col_index)+1 < BOARD_ROWS else BOARD_ROWS-1][col_index] == current_checker or get_lowest_empty_row(board, col_index) == -1:
                    pass  # redundant; safer to just check win here
                if check_win(board, current_checker):
                    print(f"Player {current_checker} won!")
                    break

        # Check for draw
        if check_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
