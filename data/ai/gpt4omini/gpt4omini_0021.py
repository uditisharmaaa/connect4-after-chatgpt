import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

def is_valid_input(col, board):
    return col.isalpha() and len(col) == 1 and 'A' <= col <= chr(65 + COLS - 1) and board[0][ord(col) - 65] == ' '

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[ord(col) - 65] == ' ':
            row[ord(col) - 65] = checker
            return True
    return False

def check_winner(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            if (col + 3 < COLS and all(board[row][col + i] == checker for i in range(4))) or \
               (row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4))) or \
               (row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == checker for i in range(4))) or \
               (row - 3 >= 0 and col + 3 < COLS and all(board[row - i][col + i] == checker for i in range(4))):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def connect_4():
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    turn_count = 0
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")

        while True:
            column_input = input().upper()
            if is_valid_input(column_input, board):
                if drop_checker(board, column_input, current_player):
                    break
                else:
                    print("Column is full. Please choose a different column.")
            else:
                print("Invalid input. Please try again.")

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = PLAYERS[turn_count % len(PLAYERS)]
        turn_count += 1

if __name__ == "__main__":
    connect_4()
