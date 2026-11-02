import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column):
    return column.isalpha() and column.upper() >= 'A' and column.upper() < chr(65 + COLS)

def get_column_index(column):
    return ord(column.upper()) - 65

def drop_checker(board, column, checker):
    col_index = get_column_index(column)
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal combinations
    for row in range(ROWS):
        for col in range(COLS):
            if (col + 3 < COLS and all(board[row][col + i] == checker for i in range(4))) or \
               (row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4))) or \
               (col + 3 < COLS and row + 3 < ROWS and all(board[row + i][col + i] == checker for i in range(4))) or \
               (col - 3 >= 0 and row + 3 < ROWS and all(board[row + i][col - i] == checker for i in range(4))):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    players_count = 2  # Fixed for submission
    players = PLAYERS[:players_count]
    current_player = random.choice(players)

    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        column = input().strip()

        while not is_valid_input(column) or not drop_checker(board, column, current_player):
            print("Invalid input. Please try again.")
            print(f"Player {current_player}, please enter a column:")
            column = input().strip()
        
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % players_count]

if __name__ == "__main__":
    main()
