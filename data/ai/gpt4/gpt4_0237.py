import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
LABELS = [chr(ord('A') + i) for i in range(COLS)]

# Helper functions
def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(LABELS))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column):
    return column in LABELS

def get_column_index(column):
    return LABELS.index(column)

def is_column_full(board, col_idx):
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx

def is_winner(board, row, col, checker):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for d in (-1, 1):  # Check both directions
            r, c = row + dr * d, col + dc * d
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                count += 1
                r, c = r + dr * d, c + dc * d
            if count >= 4:
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main Game Loop
def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column = input().strip().upper()

        if not is_valid_input(column):
            print("Invalid input, try again!")
            continue

        col_idx = get_column_index(column)

        if is_column_full(board, col_idx):
            print("Column full, try again!")
            continue

        row, col = place_checker(board, col_idx, CHECKERS[current_player])
        print_board(board)

        if is_winner(board, row, col, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if is_draw(board):
            print("Game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
