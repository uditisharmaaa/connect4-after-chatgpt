import os
import random

# Global constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_TOKENS = ["X", "O", "V", "H", "M"][:PLAYERS]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_input(col, board):
    return col in COLUMN_LABELS and board[0][COLUMN_LABELS.index(col)] == " "

def place_checker(board, col, token):
    column = COLUMN_LABELS.index(col)
    for row in reversed(board):
        if row[column] == " ":
            row[column] = token
            return True
    return False

def check_winner(board, token):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if c + 3 < COLS and all(board[r][c + i] == token for i in range(4)):
                return True
            if r + 3 < ROWS and all(board[r + i][c] == token for i in range(4)):
                return True
            if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == token for i in range(4)):
                return True
            if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == token for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {PLAYER_TOKENS[current_player]}, please enter a column:")
        col = input().strip().upper()
        if not is_valid_input(col, board):
            print("Invalid input. Try again.")
            continue
        place_checker(board, col, PLAYER_TOKENS[current_player])
        print_board(board)

        if check_winner(board, PLAYER_TOKENS[current_player]):
            print(f"Player {PLAYER_TOKENS[current_player]} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
