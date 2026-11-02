import os
import random

# CONSTANTS
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # up to 5 players
WIN_CONDITION = 4


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    # print column headers
    header = "  "
    for i in range(cols):
        header += f"  {chr(ord('A') + i)} "
    print(header)
    # print separator line
    sep_line = "+---" * cols + "+"
    for row in board:
        print(sep_line)
        line = "|"
        for cell in row:
            line += f" {cell} |"
        print(line)
    print(sep_line)


def is_valid_column_input(inp, cols):
    if len(inp) != 1:
        return False
    c = inp[0]
    if not ("A" <= c <= chr(ord("A") + cols - 1)):
        return False
    return True


def column_index_from_input(inp):
    return ord(inp[0]) - ord("A")


def place_checker(board, col, checker):
    # Start from bottom row upwards, place checker in first available empty cell
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # column full


def board_full(board):
    # If no empty cell in top row, board is full
    return all(cell != " " for cell in board[0])


def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_in_direction(r_step, c_step):
        count = 0
        r, c = row + r_step, col + c_step
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += r_step
            c += c_step
        return count

    # Directions: horiz, vert, diag1 (\), diag2 (/)
    # check horizontal
    total = 1 + count_in_direction(0, 1) + count_in_direction(0, -1)
    if total >= WIN_CONDITION:
        return True

    # check vertical
    total = 1 + count_in_direction(1, 0) + count_in_direction(-1, 0)
    if total >= WIN_CONDITION:
        return True

    # check diagonal \ (down-right & up-left)
    total = 1 + count_in_direction(1, 1) + count_in_direction(-1, -1)
    if total >= WIN_CONDITION:
        return True

    # check diagonal / (down-left & up-right)
    total = 1 + count_in_direction(1, -1) + count_in_direction(-1, 1)
    if total >= WIN_CONDITION:
        return True

    return False


def main():
    board = create_board(ROWS, COLS)

    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "

        # input validation loop
        while True:
            inp = input(prompt).strip().upper()
            if not is_valid_column_input(inp, COLS):
                # invalid input: not single uppercase letter in range
                continue
            col = column_index_from_input(inp)
            # Check if column full
            if board[0][col] != " ":  # top cell occupied means full
                # Lose turn
                break
            else:
                break

        # If column full, lose turn (print_board already printed, so just continue)
        if board[0][col] != " ":
            # no checker placed, lose turn
            # next player index
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # place checker
        r, c = place_checker(board, col, current_checker)

        # check for win
        if check_win(board, r, c, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # check for draw
        if board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        # next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
