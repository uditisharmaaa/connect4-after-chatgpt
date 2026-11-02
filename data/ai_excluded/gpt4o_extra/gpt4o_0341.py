import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(c) for c in range(65, 65 + COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def is_valid_column(col):
    return 0 <= col < COLS

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def check_win(board, piece):
    # Check horizontal
    for c in range(COLS-3):
        for r in range(ROWS):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    # Check diagonally
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def play_game():
    board = create_board()
    print_board(board)
    turn = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        col_letter = input(f"Player {PLAYERS[turn]}, please enter a column: ").upper()
        col = ord(col_letter) - 65
        
        if not is_valid_column(col):
            print("Invalid column. Try again.")
            continue

        row = get_next_open_row(board, col)
        if row is None:
            print("Column is full. Try again.")
            continue
        
        board[row][col] = PLAYERS[turn]
        print_board(board)

        if check_win(board, PLAYERS[turn]):
            print(f"Player {PLAYERS[turn]} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break

        turn = (turn + 1) % len(PLAYERS)

if __name__ == "__main__":
    play_game()
