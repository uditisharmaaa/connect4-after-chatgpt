import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # max 5 players supported

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(columns)]
    print("  " + "   ".join(labels))
    # Print board rows with separators
    row_sep = "+" + "---+" * columns
    for row in board:
        print(row_sep)
        print("| " + " | ".join(row) + " |")
    print(row_sep)

def is_valid_column(col_char, columns):
    if len(col_char) != 1 or not ('A' <= col_char <= chr(ord('A') + columns - 1)):
        return False
    return True

def column_index(col_char):
    return ord(col_char) - ord('A')

def find_row_to_place(board, col_idx):
    # Find from bottom up the first empty space in this column
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            return row
    return None  # Column full

def check_line(line, checker):
    count = 0
    for cell in line:
        if cell == checker:
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
        if check_line(board[r], checker):
            return True
    # Check vertical
    for c in range(cols):
        col = [board[r][c] for r in range(rows)]
        if check_line(col, checker):
            return True
    # Check diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            diag = [board[r + i][c + i] for i in range(4)]
            if all(cell == checker for cell in diag):
                return True
    # Check diagonal (bottom-left to top-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            diag = [board[r - i][c + i] for i in range(4)]
            if all(cell == checker for cell in diag):
                return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]

    # Randomly select starting player
    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player = players[current_player_idx]
        prompt = f"Player {player}, please enter a column: "
        col_input = input(prompt).strip().upper()

        if not is_valid_column(col_input, COLUMNS):
            # Invalid input, retry without losing turn
            continue
        
        col = column_index(col_input)
        row = find_row_to_place(board, col)

        if row is None:
            # Column full, player loses turn
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue
        
        board[row][col] = player
        print_board(board)

        if check_win(board, player):
            print(f"Player {player} won!")
            break
        
        if board_full(board):
            print("Game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
