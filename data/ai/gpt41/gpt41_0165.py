import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LENGTH = 4
MAX_COLUMNS = 26

def clear_screen():
    os.system('clear')  # or 'cls' on Windows

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    col_labels = "  " + "   ".join(string.ascii_uppercase[:COLUMNS])
    sep = "+" + "---+" * COLUMNS
    print(col_labels)
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

def get_valid_column(board, player_symbol):
    while True:
        col = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if len(col) != 1 or col not in string.ascii_uppercase[:COLUMNS]:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_idx = ord(col) - ord('A')
        if board[0][col_idx] != " ":
            print("Column is full. You lose your turn.")
            return None
        return col_idx

def place_checker(board, col_idx, checker):
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = checker
            return board.index(row), col_idx

def is_board_full(board):
    return all(cell != " " for cell in board[0])

def check_win(board, row, col, checker):
    directions = [
        (0, 1),    # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal \
        (1, -1)    # Diagonal /
    ]
    for dr, dc in directions:
        count = 1
        for d in (1, -1):
            r, c = row, col
            for _ in range(WIN_LENGTH-1):
                r += dr * d
                c += dc * d
                if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= WIN_LENGTH:
            return True
    return False

def main():
    board = create_board()
    players = PLAYER_CHECKERS.copy()
    current = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)
    while True:
        player = players[current]
        col_idx = get_valid_column(board, player)
        if col_idx is None:
            current = (current + 1) % NUM_PLAYERS
            continue
        row_idx, col_idx = place_checker(board, col_idx, player)
        clear_screen()
        print_board(board)
        if check_win(board, row_idx, col_idx, player):
            print(f"Player {player} won!")
            break
        if is_board_full(board):
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
