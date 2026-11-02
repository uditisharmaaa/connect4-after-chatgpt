import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O']  # Expand to ['X', 'O', 'V', 'H', 'M'] for more players

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column):
    return column.isalpha() and 'A' <= column <= chr(65 + COLS - 1)

def get_column_index(column):
    return ord(column) - 65

def is_column_full(board, col_index):
    return board[0][col_index] != ' '

def drop_checker(board, col_index, checker):
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                # Check horizontally
                if c <= COLS - 4 and all(board[r][c+i] == checker for i in range(4)):
                    return True
                # Check vertically
                if r <= ROWS - 4 and all(board[r+i][c] == checker for i in range(4)):
                    return True
                # Check diagonal \
                if r <= ROWS - 4 and c <= COLS - 4 and all(board[r+i][c+i] == checker for i in range(4)):
                    return True
                # Check diagonal /
                if r >= 3 and c <= COLS - 4 and all(board[r-i][c+i] == checker for i in range(4)):
                    return True
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        current_checker = CHECKERS[current_player_index]
        column = input(f"Player {current_checker}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()

        while not is_valid_input(column) or is_column_full(board, get_column_index(column)):
            print("Invalid input. Please try again.")
            column = input(f"Player {current_checker}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()

        drop_checker(board, get_column_index(column), current_checker)

        if check_winner(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break
            
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
