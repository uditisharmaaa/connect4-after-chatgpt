import os
import random

# === CONSTANTS ===
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2        # For assignment submission, set to 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_COUNT = 4
MAX_COLS = 26

assert NUM_COLS <= MAX_COLS
assert 2 <= NUM_PLAYERS <= 5

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print header
    header = "  " + "   ".join(chr(ord('A')+i) for i in range(cols))
    print(header)
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_column(input_str, board):
    cols = len(board[0])
    if len(input_str) != 1 or not input_str.isalpha():
        return -1
    col = ord(input_str.upper()) - ord('A')
    if 0 <= col < cols and board[0][col] == ' ':
        return col
    return -1

def drop_checker(board, col, checker):
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None

def check_winner(board, checker):
    rows, cols = len(board), len(board[0])
    # Horizontal, Vertical, Diagonal checks
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker: continue
            # Horizontal
            if c + WIN_COUNT <= cols and all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True
            # Vertical
            if r + WIN_COUNT <= rows and all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True
            # Diagonal /
            if r + WIN_COUNT <= rows and c - WIN_COUNT+1 >= 0:
                if all(board[r+i][c-i] == checker for i in range(WIN_COUNT)):
                    return True
            # Diagonal \
            if r + WIN_COUNT <= rows and c + WIN_COUNT <= cols:
                if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                    return True
    return False

def board_full(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS-1)

    clear_screen()
    print_board(board)

    while True:
        player = players[current]
        print(f"Player {player}, please enter a column:")
        user_input = input().strip().upper()
        col = get_valid_column(user_input, board)
        if col == -1:
            print("Invalid input. Please try again.")
            continue

        drop = drop_checker(board, col, player)
        if not drop:
            print("Column full. You lose your turn.")
        else:
            clear_screen()
            print_board(board)
            if check_winner(board, player):
                print(f"Player {player} won!")
                break
            if board_full(board):
                print("The game is a draw.")
                break
        # Next player
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
