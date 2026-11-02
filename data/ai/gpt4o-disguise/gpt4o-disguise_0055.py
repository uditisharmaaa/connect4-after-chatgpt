import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def valid_input(col, board):
    return col.isalpha() and ord(col) - 65 < COLS and board[0][ord(col) - 65] == ' '

def find_available_row(board, col):
    column_index = ord(col) - 65
    for row_index in reversed(range(ROWS)):
        if board[row_index][column_index] == ' ':
            return row_index
    return None

def check_win(board, checker):
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
            
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)) or \
               all(board[row + 3 - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_player = CHECKERS[current_player_idx]
        move = input(f"Player {current_player}, please enter a column: ").upper()
        
        while not valid_input(move, board):
            move = input(f"Invalid input! Player {current_player}, please enter a column: ").upper()
        
        row_index = find_available_row(board, move)
        board[row_index][ord(move) - 65] = current_player
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
