import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def init_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def is_valid_column(col, board):
    return col.isalpha() and 0 <= ord(col) - ord('A') < len(board[0]) and board[0][ord(col) - ord('A')] == ' '

def place_checker(board, col, checker):
    column = ord(col) - ord('A')
    for row in range(len(board)-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            break

def check_win(board, checker):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if all(board[row+n][col] == checker for n in range(4) if row+n < len(board)):
                return True
            if all(board[row][col+n] == checker for n in range(4) if col+n < len(board[0])):
                return True
            if all(board[row+n][col+n] == checker for n in range(4) if row+n < len(board) and col+n < len(board[0])):
                return True
            if all(board[row+n][col-n] == checker for n in range(4) if row+n < len(board) and col-n >= 0):
                return True
    return False

def board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = init_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS-1)
    
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        
        while True:
            col = input().strip().upper()
            if is_valid_column(col, board):
                break
            else:
                print("Invalid input. Please enter a valid column:")
        
        place_checker(board, col, CHECKERS[current_player])
        
        if check_win(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if board_full(board):
            print_board(board)
            print("Game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

main()
