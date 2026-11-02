import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

def get_valid_move(player, board):
    while True:
        move = input(f"Player {player}, please enter a column: ").upper()
        if len(move) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        if not move.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        col = ord(move) - ord('A')
        if col < 0 or col >= COLS:
            print("Invalid column. Please choose a valid column.")
            continue
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True
    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row+i][col] == checker for i in range(4)):
                return True
    # Diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    # Diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board()
    current_player = random.randint(0, PLAYERS-1)
    
    while True:
        print_board(board)
        player_checker = CHECKERS[current_player]
        col = get_valid_move(player_checker, board)
        place_checker(board, col, player_checker)
        
        if check_win(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
