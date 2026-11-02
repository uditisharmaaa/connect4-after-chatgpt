import os
import random

NUM_ROWS = 6
NUM_COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_input(input, cols):
    if len(input) != 1:
        return False
    if not input.isalpha():
        return False
    if ord(input) - 65 >= cols:
        return False
    return True

def place_checker(board, col, checker):
    column_index = ord(col) - 65
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return True
    return False

def check_for_win(board, checker):
    rows, cols = len(board), len(board[0])
    for r in range(rows):
        for c in range(cols):
            if (c <= cols - 4 and all(board[r][c + i] == checker for i in range(4))) or \
               (r <= rows - 4 and all(board[r + i][c] == checker for i in range(4))) or \
               (r <= rows - 4 and c <= cols - 4 and all(board[r + i][c + i] == checker for i in range(4))) or \
               (r >= 3 and c <= cols - 4 and all(board[r - i][c + i] == checker for i in range(4))):
                return True
    return False

def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = initialize_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randrange(PLAYERS)
    player_symbols = CHECKERS[:PLAYERS]

    print_board(board)
    
    while True:
        print(f"Player {player_symbols[current_player_index]}, please enter a column:")
        user_input = input().strip()
        
        while not is_valid_input(user_input, NUM_COLS):
            print("Invalid input. Please enter a valid column:")
            user_input = input().strip()
        
        if place_checker(board, user_input, player_symbols[current_player_index]):
            print_board(board)
            if check_for_win(board, player_symbols[current_player_index]):
                print(f"Player {player_symbols[current_player_index]} won!")
                break
            elif check_for_draw(board):
                print("The game is a draw!")
                break
            
            current_player_index = (current_player_index + 1) % PLAYERS
        else:
            print("Column is full. You lose your turn.")

main()
