import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    clear_screen()
    # print column headers
    header = "  "
    for c in range(len(board[0])):
        header += chr(ord('A') + c) + "   "
    print(header)
    # print board with separators
    sep = "+" + "---+" * len(board[0])
    for r in range(len(board)):
        print(sep)
        row_str = "|"
        for c in range(len(board[0])):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(sep)

def is_valid_column(input_str, board):
    if len(input_str) != 1:
        return False
    c = input_str.upper()
    if not ('A' <= c <= chr(ord('A') + len(board[0]) -1)):
        return False
    col_idx = ord(c) - ord('A')
    # check if column is full
    if board[0][col_idx] != " ":
        return False
    return True

def place_checker(board, col, checker):
    col_idx = ord(col) - ord('A')
    # start from bottom row to place the checker
    for row in range(len(board)-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx  # return position of placed checker
    # column is full
    return None, None

def check_line(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row = start_row
    col = start_col
    while 0 <= row < len(board) and 0 <= col < len(board[0]):
        if board[row][col] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        row += delta_row
        col += delta_col
    return False

def check_win(board, row, col, checker):
    # check horizontal (delta_row=0, delta_col=1)
    if check_line(board, row, 0, 0, 1, checker):
        return True
    # check vertical (delta_row=1, delta_col=0)
    if check_line(board, 0, col, 1, 0, checker):
        return True
    # check diagonal /
    start_row = row
    start_col = col
    while start_row > 0 and start_col < len(board[0]) - 1:
        start_row -= 1
        start_col += 1
    if check_line(board, start_row, start_col, 1, -1, checker):
        return True
    # check diagonal \
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    if check_line(board, start_row, start_col, 1, 1, checker):
        return True
    return False

def check_draw(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        input_prompt = "Player {}, please enter a column: ".format(current_checker)
        col_input = input(input_prompt).upper()

        if not is_valid_column(col_input, board):
            # if the column input is invalid or full, ask again
            while True:
                if not is_valid_column(col_input, board):
                    if len(col_input) != 1 or not ('A' <= col_input <= chr(ord('A') + COLS - 1)):
                        col_input = input("Invalid input. Please enter a valid column: ").upper()
                    else:
                        # column is full
                        print("Column is full. You lose your turn.")
                        break
                else:
                    break
            else:
                # this else never triggers since break or continue stops loop
                pass

            # Check if column was full:
            if len(col_input) == 1 and ('A' <= col_input <= chr(ord('A') + COLS - 1)):
                # column full, lose turn
                current_player_idx = (current_player_idx + 1) % PLAYERS
                print_board(board)
                continue
            else:
                # column input corrected
                pass

        # place checker if valid and column not full
        pos = place_checker(board, col_input, current_checker)
        if pos == (None, None):
            # column full: lose turn
            print("Column is full. You lose your turn.")
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)
        row_placed, col_placed = pos

        # check win
        if check_win(board, row_placed, col_placed, current_checker):
            print("Player {} won!".format(current_checker))
            break

        # check draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # next player turn
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
