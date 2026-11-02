import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2

symbols = ["X", "O", "V", "H", "M"]
players_symbols = symbols[:PLAYERS]

def create_board():
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(map(chr, range(65, 65 + COLS))))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def check_valid_column(col, board):
    if col.isalpha() and 'A' <= col <= chr(64 + COLS):
        col_index = ord(col) - 65
        if board[0][col_index] == " ":
            return True
    return False

def get_next_open_row(col_index, board):
    for r in reversed(range(ROWS)):
        if board[r][col_index] == " ":
            return r
    return None

def drop_piece(board, row, col, symbol):
    board[row][col] = symbol

def winning_move(board, symbol):
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == symbol and board[r][c+1] == symbol and board[r][c+2] == symbol and board[r][c+3] == symbol:
                return True
    
    for r in range(ROWS-3):
        for c in range(COLS):
            if board[r][c] == symbol and board[r+1][c] == symbol and board[r+2][c] == symbol and board[r+3][c] == symbol:
                return True
    
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == symbol and board[r+1][c+1] == symbol and board[r+2][c+2] == symbol and board[r+3][c+3] == symbol:
                return True
    
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == symbol and board[r-1][c+1] == symbol and board[r-2][c+2] == symbol and board[r-3][c+3] == symbol:
                return True

def is_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    print_board(board)
    current_player = random.choice(range(PLAYERS))

    while True:
        print(f"Player {players_symbols[current_player]}, please enter a column:")
        col = input().upper()

        if check_valid_column(col, board):
            col_index = ord(col) - 65
            row = get_next_open_row(col_index, board)
            if row is not None:
                drop_piece(board, row, col_index, players_symbols[current_player])
                print_board(board)

                if winning_move(board, players_symbols[current_player]):
                    print(f"Player {players_symbols[current_player]} won!")
                    break

                if is_draw(board):
                    print("The game is a draw!")
                    break
                
                current_player = (current_player + 1) % PLAYERS
            else:
                print("Column is full, you lose your turn.")
        else:
            print("Invalid input. Please enter a valid column letter.")

if __name__ == "__main__":
    main()
