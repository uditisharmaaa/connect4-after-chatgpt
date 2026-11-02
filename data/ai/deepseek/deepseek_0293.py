import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    print("+" + "+".join(["---" for _ in range(COLS)]) + "+")
    for row in board:
        print("|" + "|".join([f" {cell} " for cell in row]) + "|")
        print("+" + "+".join(["---" for _ in range(COLS)]) + "+")

def get_valid_move(board):
    valid_cols = [chr(65 + i) for i in range(COLS)]
    while True:
        move = input(f"Player {current_player}, please enter a column: ").upper()
        if move in valid_cols:
            col = ord(move) - ord('A')
            if board[0][col] == " ":
                return col
            else:
                print("Column is full!")
        else:
            print("Invalid column!")

def place_checker(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    global current_player
    board = initialize_board()
    players = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
    current_player = random.choice(players)
    
    while True:
        print_board(board)
        col = get_valid_move(board)
        place_checker(board, col, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
            
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
