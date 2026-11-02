import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(65 + i) for i in range(len(board[0]))]))
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_move(board, column):
    return column >= 0 and column < len(board[0]) and board[0][column] == " "

def make_move(board, column, symbol):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = symbol
            break

def check_winner(board, symbol):
    # Horizontal check
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == symbol and row[i+1] == symbol and row[i+2] == symbol and row[i+3] == symbol:
                return True
    
    # Vertical check
    for c in range(len(board[0])):
        for r in range(len(board) - 3):
            if board[r][c] == symbol and board[r+1][c] == symbol and board[r+2][c] == symbol and board[r+3][c] == symbol:
                return True
    
    # Diagonal check (positive slope)
    for r in range(len(board) - 3):
        for c in range(len(board[0]) - 3):
            if board[r][c] == symbol and board[r+1][c+1] == symbol and board[r+2][c+2] == symbol and board[r+3][c+3] == symbol:
                return True
    
    # Diagonal check (negative slope)
    for r in range(3, len(board)):
        for c in range(len(board[0]) - 3):
            if board[r][c] == symbol and board[r-1][c+1] == symbol and board[r-2][c+2] == symbol and board[r-3][c+3] == symbol:
                return True
    
    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)
    symbols = PLAYER_SYMBOLS[:PLAYERS]
    
    print_board(board)
    
    while True:
        print(f"Player {symbols[current_player]}, please enter a column:")
        move = input().strip().upper()
        if len(move) == 1 and move.isalpha():
            column = ord(move) - 65
            if is_valid_move(board, column):
                make_move(board, column, symbols[current_player])
                print_board(board)
                
                if check_winner(board, symbols[current_player]):
                    print(f"Player {symbols[current_player]} won!")
                    break
                
                if check_draw(board):
                    print("The game is a draw!")
                    break
                
                current_player = (current_player + 1) % PLAYERS
            else:
                print("Invalid move. Try again.")
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    main()
