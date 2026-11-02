import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear' if os.name == 'posix' else 'cls')
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def is_valid_input(col):
    return len(col) == 1 and 'A' <= col <= chr(65 + COLS - 1)

def place_checker(board, col, checker):
    col_idx = ord(col) - ord('A')
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        col = input(f"Player {checker}, please enter a column: ").upper()
        
        if not is_valid_input(col):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        if not place_checker(board, col, checker):
            print("Column is full. Try another column.")
            continue
        
        print_board(board)
        
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
