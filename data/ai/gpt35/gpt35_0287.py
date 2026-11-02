import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Max 5 players
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers A, B, C, ...
    header = "  "
    for c in range(cols):
        header += f" {string.ascii_uppercase[c]}  "
    print(header)

    # Print the board rows with separators
    separator = "+" + "---+" * cols
    for r in range(rows):
        print(separator)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(separator)

def get_valid_column_input(board, player_checker):
    cols = len(board[0])
    letters = string.ascii_uppercase[:cols]
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            continue
        if user_input not in letters:
            continue
        
        col = letters.index(user_input)
        # Check if column is full
        if board[0][col] != " ":
            # Column full, player loses turn per assignment instructions.
            return None
        return col

def place_checker(board, col, checker):
    # Place checker in the lowest free spot in the column
    rows = len(board)
    for r in range(rows-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return (r, col)
    # Should never reach here since we checked for full column before
    return None

def check_winner(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(row, col, drow, dcol):
        count = 0
        r, c = row, col
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += drow
            c += dcol
        return count

    # Check horizontal (left + right - 1 to avoid counting current position twice)
    hor_count = count_direction(row, col, 0, -1) + count_direction(row, col, 0, 1) - 1
    if hor_count >= WIN_COUNT:
        return True
    # Check vertical (up + down - 1)
    ver_count = count_direction(row, col, -1, 0) + count_direction(row, col, 1, 0) - 1
    if ver_count >= WIN_COUNT:
        return True
    # Check diagonal top-left to bottom-right
    diag1_count = count_direction(row, col, -1, -1) + count_direction(row, col, 1, 1) - 1
    if diag1_count >= WIN_COUNT:
        return True
    # Check diagonal bottom-left to top-right
    diag2_count = count_direction(row, col, 1, -1) + count_direction(row, col, -1, 1) - 1
    if diag2_count >= WIN_COUNT:
        return True

    return False

def is_draw(board):
    # If top row has no empty spaces, board is full
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = PLAYERS
    checkers = CHECKERS[:players]

    current_player_index = random.randint(0, players - 1)
    print_board(board)

    while True:
        current_checker = checkers[current_player_index]
        col = get_valid_column_input(board, current_checker)
        if col is None:
            # Column full, lose turn
            current_player_index = (current_player_index + 1) % players
            continue

        position = place_checker(board, col, current_checker)
        print_board(board)

        row, c = position
        if check_winner(board, row, c, current_checker):
            print(f"Player {current_checker} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % players

if __name__ == "__main__":
    main()
