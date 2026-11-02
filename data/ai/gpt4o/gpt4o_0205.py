import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == " "

def make_move(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_winner(board, checker):
    # Horizontal, Vertical & Diagonal checks
    for r in range(ROWS):
        for c in range(COLS):
            if c <= COLS - 4 and all(board[r][c+i] == checker for i in range(4)):
                return True
            if r <= ROWS - 4 and all(board[r+i][c] == checker for i in range(4)):
                return True
            if c <= COLS - 4 and r <= ROWS - 4 and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            if c >= 3 and r <= ROWS - 4 and all(board[r+i][c-i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(CHECKERS)
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        
        while True:
            try:
                col = ord(input().strip().upper()) - 65
                if is_valid_move(board, col):
                    break
                print("Invalid move. Try again.")
            except (IndexError, ValueError):
                print("Invalid input. Try again.")

        if make_move(board, col, current_player):
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print_board(board)
                print("Game is a draw!")
                break

            current_index = CHECKERS.index(current_player)
            current_player = CHECKERS[(current_index + 1) % PLAYERS]

if __name__ == "__main__":
    main()
