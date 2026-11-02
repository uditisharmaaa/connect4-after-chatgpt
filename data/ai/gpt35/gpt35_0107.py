import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Between 2 and 5 allowed
CHECKERS = ["X", "O", "V", "H", "M"]  # Player symbols
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(headers)
    # Print board rows with separators
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * len(board[0]) + "+")

def is_valid_column(col_char, columns):
    # Check if input is a single uppercase letter in the column range
    if len(col_char) != 1 or not col_char.isalpha() or not col_char.isupper():
        return False
    index = ord(col_char) - ord('A')
    return 0 <= index < columns

def get_column_index(col_char):
    return ord(col_char) - ord('A')

def place_checker(board, col, checker):
    # Place from bottom to top
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column full, no space

def check_line_win(line, checker):
    count = 0
    for cell in line:
        if cell == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    return False

def check_win(board, row, col, checker):
    rows = len(board)
    columns = len(board[0])

    # Horizontal check
    horizontal_line = board[row]
    if check_line_win(horizontal_line, checker):
        return True

    # Vertical check
    vertical_line = [board[r][col] for r in range(rows)]
    if check_line_win(vertical_line, checker):
        return True

    # Diagonal checks
    # Diagonal 1: top-left to bottom-right
    diag1 = []
    start_r = row
    start_c = col
    while start_r > 0 and start_c > 0:
        start_r -= 1
        start_c -= 1
    r, c = start_r, start_c
    while r < rows and c < columns:
        diag1.append(board[r][c])
        r += 1
        c += 1
    if check_line_win(diag1, checker):
        return True

    # Diagonal 2: bottom-left to top-right
    diag2 = []
    start_r = row
    start_c = col
    while start_r < rows -1 and start_c > 0:
        start_r += 1
        start_c -= 1
    r, c = start_r, start_c
    while r >= 0 and c < columns:
        diag2.append(board[r][c])
        r -= 1
        c += 1
    if check_line_win(diag2, checker):
        return True

    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column:")

        valid_input = False
        column = -1
        while not valid_input:
            user_input = input().strip()
            if not is_valid_column(user_input, COLUMNS):
                print(f"Invalid input. Please enter a column letter between A and {chr(ord('A')+COLUMNS-1)}:")
                continue
            column = get_column_index(user_input)
            # Check if column is full
            if board[0][column] != " ":
                # Turn lost
                valid_input = True  # but loses turn
                column = -1
            else:
                valid_input = True

        if column == -1:
            # Column full, player loses turn
            print_board(board)
            current_player_index = (current_player_index + 1) % PLAYERS
            continue

        row_placed = place_checker(board, column, current_checker)
        print_board(board)

        # Check win condition
        if check_win(board, row_placed, column, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if board_full(board):
            print("Game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
