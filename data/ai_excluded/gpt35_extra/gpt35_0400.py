import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

# Set for this assignment
NUM_PLAYERS = 2

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    rows = len(board)
    # Print column letters (A-G)
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(col_labels))
    # Print each row and separating lines
    line_sep = "+" + "---+" * cols
    for r in range(rows):
        print(line_sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(" " + board[r][c] + " ")
        print("|" + "|".join(row_cells) + "|")
    print(line_sep)

def choose_starting_player(num_players):
    return random.randint(0, num_players - 1)

def input_column(current_player, cols, board):
    col_letters = [chr(ord('A') + i) for i in range(cols)]
    prompt = f"Player {CHECKERS[current_player]}, please enter a column: "
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) != 1:
            continue
        if user_input not in col_letters:
            continue
        col = ord(user_input) - ord('A')
        # Check if column is full
        if board[0][col] != " ":
            # Turn lost for full column (invalid input counts as re-asking, but full column loses turn)
            return None
        return col

def place_checker(board, col, checker):
    # Place checker in the lowest available spot in the column
    rows = len(board)
    for r in reversed(range(rows)):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    # Should never reach here if place_checker called correctly
    return None

def check_direction(board, start_row, start_col, delta_r, delta_c, checker):
    count = 0
    r, c = start_row, start_col
    rows = len(board)
    cols = len(board[0])
    # Count consecutive checkers in positive delta direction
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += delta_r
        c += delta_c
    return count

def check_win(board, row, col, checker):
    # Check all 4 directions for 4 in a row including the placed checker:
    # Horizontal (0,1), Vertical(1,0), Diagonal1(1,1), Diagonal2(1,-1)
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        # Count checkers in one direction
        count_pos = check_direction(board, row, col, dr, dc, checker)
        # Count checkers in opposite direction minus 1 (because start cell counted twice)
        count_neg = check_direction(board, row, col, -dr, -dc, checker)
        total = count_pos + count_neg - 1
        if total >= WIN_COUNT:
            return True
    return False

def board_full(board):
    # If top row has any space, board not full
    return all(cell != " " for cell in board[0])

def main():
    # Validate constant requirements for this assignment
    assert ROWS == 6 and COLUMNS == 7 and NUM_PLAYERS == 2
    assert 2 <= NUM_PLAYERS <= 5

    board = create_board(ROWS, COLUMNS)
    current_player = choose_starting_player(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)
        col = input_column(current_player, COLUMNS, board)
        if col is None:
            # Full column: lose turn, no placement
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        row, col = place_checker(board, col, CHECKERS[current_player])

        if check_win(board, row, col, CHECKERS[current_player]):
            clear_screen()
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
