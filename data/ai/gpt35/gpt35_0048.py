import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Set to 2 as per submission requirement
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  " + "   ".join(COLUMN_LABELS)
    print(header)
    # Print row separator + board rows
    sep = "+" + "---+" * COLS
    for row in board:
        print(sep)
        row_str = "| " + " | ".join(row) + " |"
        print(row_str)
    print(sep)

def valid_column_choice(choice):
    return choice in COLUMN_LABELS

def find_column_index(choice):
    return ord(choice) - ord('A')

def place_checker(board, col, checker):
    # Place from bottom up
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    r, c = start_row, start_col
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    return count

def check_win(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != checker:
                continue
            # Horizontal (right)
            if col + WIN_LENGTH - 1 < COLS:
                if all(board[row][col + offset] == checker for offset in range(WIN_LENGTH)):
                    return True
            # Vertical (down)
            if row + WIN_LENGTH - 1 < ROWS:
                if all(board[row + offset][col] == checker for offset in range(WIN_LENGTH)):
                    return True
            # Diagonal (down-right)
            if row + WIN_LENGTH - 1 < ROWS and col + WIN_LENGTH -1 < COLS:
                if all(board[row + offset][col + offset] == checker for offset in range(WIN_LENGTH)):
                    return True
            # Diagonal (down-left)
            if row + WIN_LENGTH - 1 < ROWS and col - (WIN_LENGTH - 1) >= 0:
                if all(board[row + offset][col - offset] == checker for offset in range(WIN_LENGTH)):
                    return True
    return False

def input_column(player):
    while True:
        choice = input(f"Player {player}, please enter a column: ").strip().upper()
        if valid_column_choice(choice):
            return choice
        else:
            # Invalid input, ask again
            continue

def main():
    board = create_board()
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS -1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        # Ask input
        col_choice = input_column(current_checker)
        col_index = find_column_index(col_choice)
        placed = place_checker(board, col_index, current_checker)

        if not placed:
            # Column full, player loses turn
            print(f"Column {col_choice} is full. Player {current_checker} loses the turn.")
            input("Press Enter to continue...")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Check win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
