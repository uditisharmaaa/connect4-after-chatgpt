import os
import random

# === CONSTANTS === #
ROWS = 6
COLUMNS = 7       # Max: 26 for A-Z
PLAYERS = 2       # Can be from 2 to 5
WIN_COUNT = 4     # How many in a row to win (always 4)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Pick checkers for current number of players
CHECKERS = PLAYER_CHECKERS[:PLAYERS]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

# === FUNCTIONS === #

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_valid_column(board, player):
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in COLUMN_LABELS:
            print("Invalid column. Please use one letter from: " + ", ".join(COLUMN_LABELS))
            continue
        col_index = COLUMN_LABELS.index(col_input)
        if board[0][col_index] != " ":
            print(f"Column {col_input} is full. You lose your turn.")
            return None   # Lose turn per assignment
        return col_index

def place_checker(board, col_index, checker):
    # Place checker in lowest empty spot
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return board.index(row), col_index  # return row,col placed
    return None  # Should not reach here if column not full

def check_win(board, checker):
    # Check all rows, columns, diagonals for WIN_COUNT in a row
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] != checker:
                continue
            # Horizontal
            if col + WIN_COUNT <= COLUMNS and all(board[row][col+i] == checker for i in range(WIN_COUNT)):
                return True
            # Vertical
            if row + WIN_COUNT <= ROWS and all(board[row+i][col] == checker for i in range(WIN_COUNT)):
                return True
            # Diagonal down-right
            if row + WIN_COUNT <= ROWS and col + WIN_COUNT <= COLUMNS and all(board[row+i][col+i] == checker for i in range(WIN_COUNT)):
                return True
            # Diagonal up-right
            if row - WIN_COUNT + 1 >= 0 and col + WIN_COUNT <= COLUMNS and all(board[row-i][col+i] == checker for i in range(WIN_COUNT)):
                return True
    return False

def is_draw(board):
    # If any top row cell is empty, not a draw
    return all(cell != " " for cell in board[0])

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)
    print(f"Player {CHECKERS[current_player]} starts!\n")

    while True:
        checker = CHECKERS[current_player]
        col_index = get_valid_column(board, checker)
        if col_index is not None:
            row_index, _ = place_checker(board, col_index, checker)
            print_board(board)

            # Check for win
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            # Check for draw
            if is_draw(board):
                print("The game is a draw!")
                break
        else:
            print_board(board)
        # Next player's turn
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
