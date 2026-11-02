import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    os.system('clear')
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)]))
    # Print board rows
    for row in board:
        print('+' + ('---+' * BOARD_COLS))
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+' + ('---+' * BOARD_COLS))

def get_col_input(player):
    while True:
        col = input(f"Player {player}, please enter a column: ").upper()
        if len(col) != 1 or col < 'A' or col > chr(65 + BOARD_COLS - 1):
            print(f"Invalid column. Please enter a letter from A to {chr(65 + BOARD_COLS - 1)}.")
            continue
        return ord(col) - ord('A')

def place_checker(board, col, player):
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Check diagonal (down-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Check diagonal (up-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col = get_col_input(current_player)
        if not place_checker(board, col, current_player):
            print("Column is full. Try another column.")
            continue
        
        print_board(board)
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
