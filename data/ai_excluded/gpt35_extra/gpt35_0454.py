import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
WIN_COUNT = 4

CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = "  "
    for c in range(len(board[0])):
        header += chr(ord('A') + c) + "   "
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in range(len(board)):
        line = "|"
        for col in range(len(board[0])):
            line += " " + board[row][col] + " |"
        print(line)
        print("+---" * len(board[0]) + "+")

def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    if not ('A' <= col_char <= chr(ord('A') + cols -1)):
        return False
    return True

def column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # column full

def check_direction(board, start_row, start_col, dr, dc, checker):
    count = 0
    r = start_row
    c = start_col
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, row, col, checker):
    # Check horizontal
    count = 1
    count += check_direction(board, row, col - 1, 0, -1, checker)
    count += check_direction(board, row, col + 1, 0, 1, checker)
    if count >= WIN_COUNT:
        return True
    # Check vertical
    count = 1
    count += check_direction(board, row - 1, col, -1, 0, checker)
    count += check_direction(board, row + 1, col, 1, 0, checker)
    if count >= WIN_COUNT:
        return True
    # Check diagonal /
    count = 1
    count += check_direction(board, row - 1, col + 1, -1, 1, checker)
    count += check_direction(board, row + 1, col - 1, 1, -1, checker)
    if count >= WIN_COUNT:
        return True
    # Check diagonal \
    count = 1
    count += check_direction(board, row - 1, col - 1, -1, -1, checker)
    count += check_direction(board, row + 1, col + 1, 1, 1, checker)
    if count >= WIN_COUNT:
        return True

    return False

def board_full(board):
    for col in range(len(board[0])):
        if not column_full(board, col):
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players_checkers = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players_checkers[current_player_index]
        input_valid = False
        while not input_valid:
            col_input = input(f"Player {player_checker}, please enter a column: ").upper()
            if not is_valid_column(col_input, COLS):
                continue
            col_num = ord(col_input) - ord('A')
            if column_full(board, col_num):
                # Turn lost, move to next player
                break
            # Valid input and column not full
            input_valid = True

        if input_valid:
            row_placed = place_checker(board, col_num, player_checker)
            print_board(board)
            if check_win(board, row_placed, col_num, player_checker):
                print(f"Player {player_checker} won!")
                break
            if board_full(board):
                print("The game is a draw!")
                break

        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
