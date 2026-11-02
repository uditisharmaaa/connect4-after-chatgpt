import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Support up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers A, B, C...
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(cols))
    print(header)
    # Print the board rows with separators
    line = '+' + '---+' * cols
    for row in board:
        print(line)
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
    print(line)

def is_valid_column(col_char, board):
    if len(col_char) != 1:
        return False
    col = ord(col_char) - ord('A')
    if 0 <= col < len(board[0]):
        # Check if there is space in the column (top cell is empty)
        return board[0][col] == ' '
    return False

def get_column_index(col_char):
    return ord(col_char) - ord('A')

def place_checker(board, col, checker):
    # Start from bottom row upwards find empty cell
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    # Column full (should not be placed if validity checked before)
    return None

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal, vertical, and diagonal lines for 4 in a row

    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Diagonal /
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    # Diagonal \
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    # If all top row cells are occupied, board full
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players_checkers = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)
    while True:
        checker = players_checkers[current_player]
        input_prompt = f"Player {checker}, please enter a column: "
        col_char = input(input_prompt).strip().upper()

        if not is_valid_column(col_char, board):
            # If out of range or column full, invalid input
            # According to the spec: if column full, lose turn; if invalid input, ask again
            col_index = ord(col_char) - ord('A') if len(col_char) == 1 else -1
            if 0 <= col_index < COLS:
                # Column valid but full -> lose turn
                # So just skip to next player
                current_player = (current_player + 1) % PLAYERS
                continue
            else:
                # Invalid input - ask again
                continue

        col = get_column_index(col_char)
        pos = place_checker(board, col, checker)
        if pos is None:
            # Column full -> lose turn (skip next player)
            current_player = (current_player + 1) % PLAYERS
            continue

        print_board(board)
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("The game is a draw.")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
