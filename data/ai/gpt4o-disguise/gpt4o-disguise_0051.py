import random
import os

ROWS = 6
COLS = 7
PLAYERS = 2

CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(row) + "+")

def get_column():
    while True:
        move = input("Please enter a column: ").upper()
        if move.isalpha() and len(move) == 1 and 'A' <= move <= chr(ord('A') + COLS - 1):
            return ord(move) - ord('A')
        else:
            print("Invalid input. Try again.")

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row][col+1] == checker and board[row][col+2] == checker and board[row][col+3] == checker:
                return True
    # Vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    # Diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    # Diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    current_player = random.choice(PLAYER_CHECKERS)
    
    print_board(board)
    
    while True:
        print(f"Player {current_player}, ", end="")
        col = get_column()
        
        if place_checker(board, col, current_player):
            print_board(board)
            
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            if check_draw(board):
                print("It's a draw!")
                break
            
            current_player = PLAYER_CHECKERS[(PLAYER_CHECKERS.index(current_player) + 1) % PLAYERS]
        else:
            print("Column is full. Player loses the turn.")
            
main()
