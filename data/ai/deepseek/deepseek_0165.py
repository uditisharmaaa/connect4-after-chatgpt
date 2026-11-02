import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Clear screen
    os.system('clear' if os.name == 'posix' else 'cls')
    # Print column labels
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    # Print board
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

def get_valid_input(current_player):
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) == 1 and 'A' <= col <= chr(65 + COLS - 1):
            return ord(col) - 65
        print(f"Invalid input. Please enter a letter from A to {chr(65 + COLS - 1)}.")

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, row, col):
    directions = [
        [(0, 1), (0, -1)],  # Horizontal
        [(1, 0), (-1, 0)],   # Vertical
        [(1, 1), (-1, -1)],  # Diagonal /
        [(1, -1), (-1, 1)]   # Diagonal \
    ]
    checker = board[row][col]
    for axis in directions:
        count = 1
        for dr, dc in axis:
            r, c = row + dr, col + dc
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                count += 1
                r += dr
                c += dc
                if count == 4:
                    return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        col = get_valid_input(CHECKERS[current_player])
        if not place_checker(board, col, CHECKERS[current_player]):
            print("Column is full. Try another column.")
            continue
        
        print_board(board)
        
        # Find the row where the checker was placed
        for row in range(ROWS):
            if board[row][col] == CHECKERS[current_player]:
                if check_win(board, row, col):
                    print(f"Player {CHECKERS[current_player]} won!")
                    return
                break
        
        if check_draw(board):
            print("Game ended in a draw!")
            return
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
