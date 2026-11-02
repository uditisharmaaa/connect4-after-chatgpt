import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    os.system('clear')
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)]))
    
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

def is_valid_column(column):
    if len(column) != 1:
        return False
    col = ord(column.upper()) - ord('A')
    return 0 <= col < BOARD_COLS

def get_valid_column(current_player):
    while True:
        column = input(f"Player {current_player}, please enter a column: ").strip()
        if is_valid_column(column):
            return ord(column.upper()) - ord('A')
        print("Invalid column. Please enter a valid column letter (A-{}).".format(chr(65 + BOARD_COLS - 1)))

def place_checker(board, col, checker):
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, row, col, checker):
    directions = [
        [(0, 1), (0, -1)],  # Horizontal
        [(1, 0), (-1, 0)],   # Vertical
        [(1, 1), (-1, -1)],  # Diagonal /
        [(1, -1), (-1, 1)]   # Diagonal \
    ]
    
    for direction_pair in directions:
        count = 1
        for dr, dc in direction_pair:
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
                count += 1
                r += dr
                c += dc
                if count == 4:
                    return True
        if count >= 4:
            return True
    return False

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        col = get_valid_column(current_player)
        if not place_checker(board, col, current_player):
            print("Column is full. You lose your turn.")
        else:
            for row in range(BOARD_ROWS):
                if board[row][col] == current_player:
                    if check_win(board, row, col, current_player):
                        print_board(board)
                        print(f"Player {current_player} won!")
                        return
                    break
        
        if is_board_full(board):
            print_board(board)
            print("The game is a draw!")
            return
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
