import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

def init_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)]))
    print('+' + ('---+' * COLS))
    for row in board:
        print('|' + ('   |' * COLS))
        print('+' + ('---+' * COLS))

def get_player_checkers(num_players):
    checkers = ['X', 'O', 'V', 'H', 'M']
    return checkers[:num_players]

def is_valid_column(col, board):
    if len(col) != 1 or not col.isalpha():
        return False
    col_idx = ord(col.upper()) - ord('A')
    return 0 <= col_idx < COLS and board[0][col_idx] == ' '

def place_checker(board, col, checker):
    col_idx = ord(col.upper()) - ord('A')
    for row in range(ROWS-1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = init_board()
    checkers = get_player_checkers(PLAYERS)
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board)
        print(f"Player {checkers[current_player]}, please enter a column: ")
        
        col = input().strip()
        while not is_valid_column(col, board):
            print_board(board)
            print(f"Invalid column. Player {checkers[current_player]}, please enter a valid column: ")
            col = input().strip()
        
        place_checker(board, col, checkers[current_player])
        
        if check_win(board, checkers[current_player]):
            print_board(board)
            print(f"Player {checkers[current_player]} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
