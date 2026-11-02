import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4

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
    row_sep = "+" + "---+" * cols
    for row in board:
        print(row_sep)
        print("| " + " | ".join(row) + " |")
    print(row_sep)

def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    if not ('A' <= col_char <= chr(ord('A') + cols - 1)):
        return False
    return True

def column_index(col_char):
    return ord(col_char) - ord('A')

def place_checker(board, col, checker):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Column full

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(r_step, c_step):
        count = 0
        r, c = row + r_step, col + c_step
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += r_step
            c += c_step
        return count

    # Check all 4 directions:
    # Horizontal (0,1) and (0,-1)
    hor = 1 + count_direction(0, 1) + count_direction(0, -1)
    if hor >= WIN_CONDITION:
        return True
    # Vertical (1,0) and (-1,0)
    ver = 1 + count_direction(1, 0) + count_direction(-1, 0)
    if ver >= WIN_CONDITION:
        return True
    # Diag1 (1,1) and (-1,-1)
    diag1 = 1 + count_direction(1, 1) + count_direction(-1, -1)
    if diag1 >= WIN_CONDITION:
        return True
    # Diag2 (1,-1) and (-1,1)
    diag2 = 1 + count_direction(1, -1) + count_direction(-1, 1)
    if diag2 >= WIN_CONDITION:
        return True

    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def get_player_input(current_player, cols):
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").upper()
        if not is_valid_column(user_input, cols):
            continue
        return column_index(user_input)

def main():
    # Validate constants to satisfy constraints
    global COLUMNS, ROWS, PLAYERS
    if COLUMNS < 1 or COLUMNS > MAX_COLUMNS:
        COLUMNS = 7
    if ROWS < 1:
        ROWS = 6
    if PLAYERS < 2:
        PLAYERS = 2
    elif PLAYERS > 5:
        PLAYERS = 5

    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    # Randomly select first player
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    game_over = False
    while not game_over:
        checker = players[current_player_index]
        col = get_player_input(checker, COLUMNS)
        placed = place_checker(board, col, checker)
        if placed is None:
            # Column full, player loses turn, proceed to next player
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        r, c = placed
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            game_over = True
            break
        if board_full(board):
            print("The game is a draw.")
            break
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
