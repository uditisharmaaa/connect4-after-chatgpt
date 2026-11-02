import os
import random

# Constants
ROWS, COLUMNS = 6, 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'] # Supports up to 5 players
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # ['A', 'B', 'C', ..., 'G']

# Board initialization
board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')  # Clear screen for Unix/Linux
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")
    print()  # Empty line for better readability

def is_valid_column(column):
    return column in COLUMN_LABELS

def get_next_open_row(col_index):
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == ' ':
            return row
    return None

def drop_checker(col_index, checker):
    row = get_next_open_row(col_index)
    if row is not None:
        board[row][col_index] = checker
    return row

def check_win(checker):
    # Check horizontal locations for win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row][col+1] == checker and board[row][col+2] == checker and board[row][col+3] == checker:
                return True

    # Check vertical locations for win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    
    return False

def is_draw():
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    print_board()
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        player_checker = CHECKERS[current_player]
        print(f"Player {player_checker}, it's your turn.")
        column = input("Please enter a column: ").strip().upper()

        if not is_valid_column(column):
            print("Invalid column. Please try again.")
            continue

        col_index = COLUMN_LABELS.index(column)
        if get_next_open_row(col_index) is None:
            print("Column is full. Please try another column.")
            continue

        drop_checker(col_index, player_checker)
        print_board()

        if check_win(player_checker):
            print(f"Player {player_checker} won!")
            break

        if is_draw():
            print("The game is a draw.")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
