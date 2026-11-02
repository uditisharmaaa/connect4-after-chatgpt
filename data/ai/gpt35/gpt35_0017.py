import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()

    # Print column headers
    headers = "  "
    for i in range(COLS):
        headers += " " + chr(ord('A') + i) + "  "
    print(headers)

    # Print board rows
    row_line = "+---" * COLS + "+"
    for row in board:
        print(row_line)
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print(row_line)

def get_valid_column(board, player_checker):
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            # Input length is not 1 character
            continue
        col_num = ord(col_input) - ord('A')
        if col_num < 0 or col_num >= COLS:
            # Out of bounds column
            continue
        if board[0][col_num] != " ":
            # Column is full, turn lost
            print(f"Column {col_input} is full. Turn lost.")
            return None  # Indicates losing turn
        return col_num

def place_checker(board, col, checker):
    # Place checker in lowest free row in this column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None, None  # Should not happen if we validated before

def check_win(board, checker):

    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - WIN_CONDITION + 1):
            count = 0
            for i in range(WIN_CONDITION):
                if board[row][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_CONDITION:
                return True

    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - WIN_CONDITION + 1):
            count = 0
            for i in range(WIN_CONDITION):
                if board[row + i][col] == checker:
                    count += 1
                else:
                    break
            if count == WIN_CONDITION:
                return True

    # Diagonal (down-right) check
    for row in range(ROWS - WIN_CONDITION + 1):
        for col in range(COLS - WIN_CONDITION + 1):
            count = 0
            for i in range(WIN_CONDITION):
                if board[row + i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_CONDITION:
                return True

    # Diagonal (down-left) check
    for row in range(ROWS - WIN_CONDITION + 1):
        for col in range(WIN_CONDITION - 1, COLS):
            count = 0
            for i in range(WIN_CONDITION):
                if board[row + i][col - i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_CONDITION:
                return True

    return False

def check_draw(board):
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]

    # Random first player
    current_player_idx = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        col = get_valid_column(board, player_checker)
        if col is None:
            # Turn lost due to full column (invalid)
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        place_checker(board, col, player_checker)
        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
