import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LENGTH = 4
MAX_COLUMNS = 26  # For A-Z

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def valid_column(col, cols):
    return len(col) == 1 and col in string.ascii_uppercase[:cols]

def get_empty_row(board, col_idx):
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            return row
    return None

def check_winner(board, row, col, checker):
    directions = [(0,1), (1,0), (1,1), (1,-1)]  # horiz, vert, diag, anti-diag
    for dr, dc in directions:
        count = 1
        for step in [1, -1]:
            r, c = row, col
            while True:
                r += dr * step
                c += dc * step
                if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                    count += 1
                    if count == WIN_LENGTH:
                        return True
                else:
                    break
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player]}, you start!")
    while True:
        checker = PLAYER_CHECKERS[current_player]
        move = ""
        while True:
            move = input(f"Player {checker}, please enter a column: ").strip().upper()
            if not valid_column(move, COLUMNS):
                print("Invalid input. Please enter a valid column letter.")
                continue
            col_idx = string.ascii_uppercase.index(move)
            empty_row = get_empty_row(board, col_idx)
            if empty_row is None:
                print("Column is full. You lose your turn.")
                empty_row = None
                break  # Lose turn
            else:
                break  # Valid
        if empty_row is not None:  # Placed successfully
            board[empty_row][col_idx] = checker
            print_board(board)
            if check_winner(board, empty_row, col_idx, checker):
                print(f"Player {checker} won!")
                break
        else:
            print_board(board)
        if board_full(board):
            print("The board is full -- it's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
