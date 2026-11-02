import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == ' '

def drop_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row+i][col] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board)
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ", end='')
        
        # Input validation
        while True:
            try:
                col = input().upper()
                if len(col) != 1 or not col.isalpha():
                    raise ValueError
                col = ord(col) - ord('A')
                if not is_valid_move(board, col):
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Try again: ", end='')
        
        # Drop checker and check win/draw
        drop_checker(board, col, checker)
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
