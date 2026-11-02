import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'] 

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear') 
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_input(choice, cols):
    if len(choice) == 1 and choice.isalpha():
        index = ord(choice.upper()) - 65
        return 0 <= index < cols
    return False

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col:col+4] == [checker]*4:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal \
    for row in range(3, len(board)):
        for col in range(3, len(board[0])):
            if all(board[row-i][col-i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def connect4():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    player_symbols = CHECKERS[:PLAYERS]

    while True:
        print_board(board)
        print(f"Player {player_symbols[current_player]}'s turn.")
        col_choice = input("Please enter a column: ").strip()

        if not is_valid_input(col_choice, COLUMNS):
            print("Invalid input. Please enter a valid column.")
            continue

        col_idx = ord(col_choice.upper()) - 65

        if place_checker(board, col_idx, player_symbols[current_player]):
            if check_win(board, player_symbols[current_player]):
                print_board(board)
                print(f"Player {player_symbols[current_player]} won!")
                break

            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break

            current_player = (current_player + 1) % PLAYERS
        else:
            print("Column is full. Turn missed.")

if __name__ == '__main__':
    connect4()
