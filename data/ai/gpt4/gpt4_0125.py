import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
MARKERS = ["X", "O", "V", "H", "M"]
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(LETTERS[:COLS]))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(col, board):
    return col.isalpha() and len(col) == 1 and LETTERS.index(col) < COLS and board[0][LETTERS.index(col)] == " "

def drop_checker(board, col, marker):
    col_idx = LETTERS.index(col)
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = marker
            return row, col_idx

def check_winner(board, marker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == marker for i in range(4)):
                return True
    # Vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == marker for i in range(4)):
                return True
    # Diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == marker for i in range(4)):
                return True
    # Diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == marker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game loop
def play_game():
    board = create_board()
    players = [MARKERS[i] for i in range(PLAYERS)]
    current_player = random.choice(players)

    print_board(board)
    print(f"Player {current_player} starts!")

    while True:
        print_board(board)
        col = input(f"Player {current_player}, please enter a column: ").strip().upper()

        if not is_valid_column(col, board):
            print("Invalid input. Try again.")
            continue

        _, _ = drop_checker(board, col, current_player)

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    play_game()
