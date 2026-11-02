import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    headers = [chr(65 + i) for i in range(COLS)]
    print('  ' + '   '.join(headers))
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * COLS)

def get_next_player(current_player):
    return (current_player + 1) % PLAYERS

def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '

def drop_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
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
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    # Diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    # Diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = initialize_board()
    current_player = random.randint(0, PLAYERS-1)
    checkers = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
    
    while True:
        print_board(board)
        print(f"Player {checkers[current_player]}, please enter a column:")
        
        try:
            col = input().strip().upper()
            if not col or len(col) != 1 or not ('A' <= col <= chr(64 + COLS)):
                raise ValueError()
            col = ord(col) - 65
        except:
            print("Invalid input. Try again.")
            continue
        
        if not is_valid_move(board, col):
            print("Column full or invalid. Try again.")
            continue
        
        drop_checker(board, col, checkers[current_player])
        
        if check_win(board, checkers[current_player]):
            print_board(board)
            print(f"Player {checkers[current_player]} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = get_next_player(current_player)

if __name__ == "__main__":
    main()
