import os
import random
import string

# Constants: board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # from 2 to 5 players supported
CHECKERS = ["X", "O", "V", "H", "M"]

WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column headers A, B, C...
    header = "  "
    for c in range(cols):
        header += "  " + string.ascii_uppercase[c] + " "
    print(header)
    # Print horizontal line pattern
    line = "+" + "---+"*cols
    # Each row with cells between lines
    for r in range(rows):
        print(line)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def get_valid_column_input(current_player, cols, board):
    while True:
        inp = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            print("Invalid input. Please enter exactly one letter corresponding to a column.")
            continue
        if inp not in string.ascii_uppercase[:cols]:
            print(f"Invalid column. Please enter a letter between A and {string.ascii_uppercase[cols-1]}.")
            continue
        col = string.ascii_uppercase.index(inp)
        # Check if column is full
        if board[0][col] != " ":
            # Player loses turn if column full
            return None  
        return col

def place_checker(board, col, checker):
    rows = len(board)
    # Place checker at the lowest empty cell in the column
    for r in range(rows-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    # This should not happen if checked beforehand
    return None

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(dr, dc):
        count = 0
        r, c = row, col
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count - 1  # minus the starting cell counted twice

    # Check horizontal (left and right)
    horiz = 1 + count_direction(0, -1) + count_direction(0, 1)
    if horiz >= WIN_LENGTH:
        return True

    # Check vertical (up and down)
    vert = 1 + count_direction(-1, 0) + count_direction(1, 0)
    if vert >= WIN_LENGTH:
        return True

    # Check diagonal /
    diag1 = 1 + count_direction(-1, 1) + count_direction(1, -1)
    if diag1 >= WIN_LENGTH:
        return True

    # Check diagonal \
    diag2 = 1 + count_direction(-1, -1) + count_direction(1, 1)
    if diag2 >= WIN_LENGTH:
        return True

    return False

def board_full(board):
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def main():
    # Validate constants just in case
    if not (2 <= PLAYERS <= 5):
        print("Number of players must be between 2 and 5.")
        return
    if not (4 <= ROWS <= 100 and 4 <= COLUMNS <= 26):
        print("Board dimensions must be minimum 4x4 and max 100x26.")
        return

    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS-1)

    print_board(board)
    while True:
        col = get_valid_column_input(current_player, COLUMNS, board)
        if col is None:
            # Column full -> lose turn
            print(f"Column is full. Player {CHECKERS[current_player]} loses the turn.")
            # Do not place checker, just change player
        else:
            pos = place_checker(board, col, CHECKERS[current_player])
            print_board(board)
            if check_win(board, pos[0], pos[1], CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            if board_full(board):
                print("Game is a draw.")
                break
        # Next player's turn
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
