import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def clear_screen():
    os.system('clear')

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_valid_column(board):
    while True:
        try:
            col = input("Please enter a column: ").strip().upper()
            if len(col) != 1 or not ('A' <= col <= chr(65 + COLS - 1)):
                raise ValueError
            col_index = ord(col) - 65
            if board[0][col_index] != ' ':
                print("Column is full. Try another one.")
                continue
            return col_index
        except ValueError:
            print("Invalid column. Please try again.")

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = initialize_board()
    players_checkers = CHECKERS[:MAX_PLAYERS]
    current_player = random.randint(0, MAX_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        print(f"Player {players_checkers[current_player]}'s turn.")
        col = get_valid_column(board)
        place_checker(board, col, players_checkers[current_player])
        print_board(board)

        if check_win(board, players_checkers[current_player]):
            print(f"Player {players_checkers[current_player]} won!")
            break
        elif check_draw(board):
            print("The game is a draw.")
            break

        current_player = (current_player + 1) % MAX_PLAYERS

if __name__ == "__main__":
    main()
