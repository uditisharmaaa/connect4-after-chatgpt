import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

def valid_input(col):
    return col.isalpha() and col.upper() >= 'A' and col.upper() <= chr(65 + COLS - 1)

def get_column_index(col):
    return ord(col.upper()) - 65

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[get_column_index(col)] == ' ':
            row[get_column_index(col)] = checker
            return True
    return False

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if (c + 3 < COLS and
                board[r][c] == checker and
                board[r][c + 1] == checker and
                board[r][c + 2] == checker and
                board[r][c + 3] == checker):
                return True
            if (r + 3 < ROWS and
                board[r][c] == checker and
                board[r + 1][c] == checker and
                board[r + 2][c] == checker and
                board[r + 3][c] == checker):
                return True
            if (r + 3 < ROWS and c + 3 < COLS and
                board[r][c] == checker and
                board[r + 1][c + 1] == checker and
                board[r + 2][c + 2] == checker and
                board[r + 3][c + 3] == checker):
                return True
            if (r - 3 >= 0 and c + 3 < COLS and
                board[r][c] == checker and
                board[r - 1][c + 1] == checker and
                board[r - 2][c + 2] == checker and
                board[r - 3][c + 3] == checker):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        
        col = input().strip()
        while not valid_input(col) or not place_checker(board, col, current_player):
            print("Invalid input. Please retry.")
            col = input().strip()
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
