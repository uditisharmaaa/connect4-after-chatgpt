import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    sep = "+" + "---+" * cols
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

def ask_player_column(player_checker, cols, board):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            print("Invalid input, please enter exactly one letter corresponding to a column.")
            continue
        col = ord(inp) - ord('A')
        if col < 0 or col >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A')+cols-1)}.")
            continue
        # Check if column is full
        if board[0][col] != " ":
            print(f"Column {inp} is full, you lose your turn.")
            return -1
        return col

def place_checker(board, col, checker):
    # Place checker in the lowest empty row in col
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return -1, -1  # Should never happen if checked before

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Check diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    # Check diagonal (down-left)
    for r in range(rows - 3):
        for c in range(3, cols):
            if all(board[r + i][c - i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = players[current_idx]
        col = ask_player_column(current_checker, COLS, board)
        if col == -1:
            # lose turn, advance player
            current_idx = (current_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        place_checker(board, col, current_checker)
        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
