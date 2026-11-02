import os
import random

# Constants (for submission: 6 rows, 7 columns, 2 players)
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # between 2 and 5 allowed
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers (A, B, C, ...)
    header = "  "
    for c in range(len(board[0])):
        header += "  " + chr(ord('A') + c) + " "
    print(header)

    # Print board with grid lines
    row_count = len(board)
    col_count = len(board[0])
    sep_line = "+" + "---+" * col_count

    for r in range(row_count):
        print(sep_line)
        row_str = "|"
        for c in range(col_count):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(sep_line)

def valid_column_input(inp, columns):
    if len(inp) != 1:
        return False
    c = inp.upper()
    if c < 'A' or c >= chr(ord('A') + columns):
        return False
    return True

def column_index_from_letter(letter):
    return ord(letter.upper()) - ord('A')

def place_checker(board, column, checker):
    # Board rows start at top index 0, but checker falls to lowest empty cell (higher row indices)
    # so insert from the bottom upwards
    for r in range(len(board)-1, -1, -1):
        if board[r][column] == " ":
            board[r][column] = checker
            return True
    # column full
    return False

def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def four_in_a_row(lst, checker):
    count = 0
    for x in lst:
        if x == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        row_line = board[r]
        if four_in_a_row(row_line, checker):
            return True

    # Check vertical
    for c in range(cols):
        col_line = [board[r][c] for r in range(rows)]
        if four_in_a_row(col_line, checker):
            return True

    # Check \ diagonals (bottom-left to top-right)
    # Iterate over every possible diagonal with length >= 4
    for r in range(rows-3):
        for c in range(cols-3):
            diagonal = [board[r+i][c+i] for i in range(4)]
            if all(cell == checker for cell in diagonal):
                return True

    # Check / diagonals (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols-3):
            diagonal = [board[r-i][c+i] for i in range(4)]
            if all(cell == checker for cell in diagonal):
                return True

    return False

def random_start_player(num_players):
    return random.randint(0, num_players - 1)

def next_player(current, num_players):
    return (current + 1) % num_players

def get_player_input(player_checker, columns):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not valid_column_input(inp, columns):
            # invalid input
            continue
        return inp

def main():
    board = create_board(ROWS, COLUMNS)
    players_checkers = CHECKERS[:PLAYERS]

    current_player = random_start_player(PLAYERS)

    print_board(board)

    while True:
        checker = players_checkers[current_player]

        col_letter = get_player_input(checker, COLUMNS)
        col_idx = column_index_from_letter(col_letter)

        # Attempt to place checker
        placed = place_checker(board, col_idx, checker)

        # If column full, player loses turn (do not place checker)
        # but still change player turn
        if not placed:
            current_player = next_player(current_player, PLAYERS)
            print_board(board)
            continue

        print_board(board)

        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player turn
        current_player = next_player(current_player, PLAYERS)

if __name__ == "__main__":
    main()
