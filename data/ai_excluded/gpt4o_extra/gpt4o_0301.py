import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

# Initialize board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    header = '  ' + '   '.join(chr(i) for i in range(ord('A'), ord('A') + COLS))
    print(header)
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def is_winner(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal checks
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    checkers = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    
    while True:
        print(f"Player {checkers[current_player]}, please enter a column:")
        try:
            col = input().strip().upper()
            if len(col) != 1 or not ('A' <= col <= 'G'):
                print("Invalid input. Try again.")
                continue
            col_idx = ord(col) - ord('A')
            if not drop_checker(board, col_idx, checkers[current_player]):
                print("Column full. Turn lost.")
            else:
                print_board(board)
                if is_winner(board, checkers[current_player]):
                    print(f"Player {checkers[current_player]} won!")
                    break
                if is_draw(board):
                    print("It's a draw!")
                    break
                current_player = (current_player + 1) % PLAYERS
        except Exception as e:
            print("Invalid input, please enter a valid column letter.")

if __name__ == "__main__":
    main()
