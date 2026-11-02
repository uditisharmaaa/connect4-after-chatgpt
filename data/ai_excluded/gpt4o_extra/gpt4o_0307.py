import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(c + ord('A')) for c in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(column):
    return column.isalpha() and ord(column) >= ord('A') and ord(column) < ord('A') + COLUMNS

def get_column_number(column):
    return ord(column) - ord('A')

def is_valid_move(board, column):
    return board[0][column] == ' '

def drop_checker(board, checker, column):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_for_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Check diagonal /
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    # Check diagonal \
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def main():
    board = create_board()
    current_turn = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = CHECKERS[current_turn]
        print(f"Player {player_checker}, please enter a column: ", end='')
        player_input = input().strip().upper()

        if not is_valid_input(player_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        column_number = get_column_number(player_input)

        if not is_valid_move(board, column_number):
            print("Column is full. Select another.")
            continue

        drop_checker(board, player_checker, column_number)
        print_board(board)

        if check_for_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_for_draw(board):
            print("The game is a draw!")
            break

        current_turn = (current_turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
