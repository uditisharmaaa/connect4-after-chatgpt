import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"]  # Support up to 5 players
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS[:len(board[0])]))
    # Print top border line
    print('+' + '---+' * len(board[0]))
    # Print rows
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def is_valid_column(col_label, cols):
    if len(col_label) != 1:
        return False
    if col_label < 'A' or col_label >= chr(ord('A') + cols):
        return False
    return True

def get_column_index(col_label):
    return ord(col_label) - ord('A')

def column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place checker in lowest available row in column col
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    # Column full, no placement
    return None

def check_line(board, start_row, start_col, d_row, d_col, checker):
    count = 0
    r, c = start_row, start_col
    while 0 <= r < len(board) and 0 <= c < len(board[0]):
        if board[r][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        r += d_row
        c += d_col
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Horizontal check
    for r in range(rows):
        if check_line(board, r, 0, 0, 1, checker):
            return True
    # Vertical check
    for c in range(cols):
        if check_line(board, 0, c, 1, 0, checker):
            return True
    # Diagonal down-right check
    for r in range(rows):
        for c in range(cols):
            # Check if there is space for 4 diagonal elements
            if r + WIN_COUNT - 1 < rows and c + WIN_COUNT - 1 < cols:
                if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                    return True
    # Diagonal up-right check
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols):
            if c + WIN_COUNT - 1 < cols:
                if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                    return True
    return False

def check_draw(board):
    # Draw if no empty space in top row (means board filled)
    return all(cell != " " for cell in board[0])

def get_valid_input(current_player):
    while True:
        try:
            col_label = input(f"Player {current_player}, please enter a column: ").upper()
        except EOFError:
            # If input stream ends unexpectedly, just exit program
            exit()
        if not is_valid_column(col_label, COLS):
            continue
        col = get_column_index(col_label)
        return col, col_label

def main():
    board = create_board(ROWS, COLS)
    players = PLAYERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = players[current_player_index]

        col, col_label = get_valid_input(current_checker)

        if column_full(board, col):
            # Turn lost if column full
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        row = place_checker(board, col, current_checker)
        print_board(board)

        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
