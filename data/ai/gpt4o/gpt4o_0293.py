import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(i + 65) for i in range(COLUMNS)]

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(input):
    return input in COLUMN_LABELS

def place_checker(board, column, checker):
    col_index = COLUMN_LABELS.index(column)
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False

def check_for_win(board, checker):
    # Horizontal, vertical, and diagonal checks
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (c + 3 < COLUMNS and all(board[r][c + i] == checker for i in range(4))) or \
               (r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4))) or \
               (c + 3 < COLUMNS and r + 3 < ROWS and all(board[r + i][c + i] == checker for i in range(4))) or \
               (c - 3 >= 0 and r + 3 < ROWS and all(board[r + i][c - i] == checker for i in range(4))):
                return True
    return False

def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)
    
def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.choice(range(PLAYERS))
    print_board(board)

    while True:
        player_checker = CHECKERS[current_player]
        col_input = input(f"Player {player_checker}, please enter a column: ")

        while not is_valid_input(col_input) or not place_checker(board, col_input, player_checker):
            col_input = input(f"Invalid input! Player {player_checker}, please enter a column: ")

        print_board(board)

        if check_for_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_for_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
