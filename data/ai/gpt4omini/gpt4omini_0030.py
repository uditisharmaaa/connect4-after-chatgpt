import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = ['X', 'O']  # Can be extended for more players

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels A to G
    print("+---" + "+---" * (COLUMNS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLUMNS - 1) + "+")

def is_valid_input(column_input):
    if len(column_input) != 1:
        return False
    if column_input not in (chr(65 + i) for i in range(COLUMNS)):
        return False
    return True

def get_column_index(column_input):
    return ord(column_input) - 65

def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal \
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal /
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    game_over = False

    print_board(board)
    
    while not game_over:
        print(f"Player {current_player}, please enter a column:")
        
        while True:
            column_input = input().upper()
            if is_valid_input(column_input):
                column_index = get_column_index(column_input)
                if drop_checker(board, column_index, current_player):
                    break
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input, please enter a valid column (A-G).")
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif is_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
