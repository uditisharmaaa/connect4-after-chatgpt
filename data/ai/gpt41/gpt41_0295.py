import os
import random
import string

# --------- CONSTANTS ----------
ROWS = 6
COLUMNS = 7
MAX_COLS = 26  # Max columns (A-Z)
PLAYERS = 2    # Set to 2 for submission; can be up to 5

CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

# --------- FUNCTIONS ----------

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    print("+" + "---+"*cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+"*cols)

def random_first_player():
    return random.randint(0, PLAYERS - 1)

def is_valid_column(input_col, board):
    if not input_col.isalpha() or len(input_col) != 1:
        return False
    col_index = ord(input_col.upper()) - ord('A')
    if col_index < 0 or col_index >= len(board[0]):
        return False
    # Check if column is not full
    return board[0][col_index] == " "

def get_next_open_row(board, col):
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return None  # Column full

def drop_checker(board, row, col, checker):
    board[row][col] = checker

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Check positive diagonal
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    # Check negative diagonal
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True

    return False

def is_board_full(board):
    return all(cell != " " for cell in board[0])

def get_column_input(player_checker, board):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if is_valid_column(user_input, board):
            col = ord(user_input) - ord('A')
            if get_next_open_row(board, col) is not None:
                return col
            else:
                print(f"Column {user_input} is full! You lose your turn!")
                return None  # Lose turn if column full
        else:
            print("Invalid input. Please enter a valid column letter (A-{}) that is not full.".format(
                chr(ord('A')+len(board[0])-1)))

# --------- MAIN GAME LOOP ----------

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random_first_player()
    print_board(board)
    print(f"Player {CHECKERS[current_player]} starts!")

    game_over = False
    turn = 0

    while not game_over:
        print_board(board)
        player_checker = CHECKERS[current_player]
        col = get_column_input(player_checker, board)
        if col is None:
            # Lose turn if input is valid but column is full
            current_player = (current_player + 1) % PLAYERS
            continue
        row = get_next_open_row(board, col)
        drop_checker(board, row, col, player_checker)

        if check_win(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            game_over = True
            break

        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == '__main__':
    main()
