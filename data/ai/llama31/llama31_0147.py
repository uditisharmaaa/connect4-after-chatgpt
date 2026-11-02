import os
import random

# Constant variables
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with whitespaces"""
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    print('+---+---+---+---+---+---+---+')
    for row in board:
        print('|', end='')
        for cell in row:
            print(' ' + cell + ' |', end='')
        print()
        print('+---+---+---+---+---+---+---+')
    print()

def get_player_checker(player_num):
    """Get the checker symbol for a player"""
    return CHECKERS[player_num - 1]

def is_valid_input(input_str):
    """Check if user input is a valid column letter"""
    return input_str.upper() in 'ABCDEFG'

def get_column_num(input_str):
    """Convert column letter to column number"""
    return ord(input_str.upper()) - ord('A')

def is_column_full(board, col_num):
    """Check if a column is full"""
    return board[NUM_ROWS - 1][col_num]!= ' '

def place_checker(board, player_num, col_num):
    """Place a checker in a column"""
    for row_num in range(NUM_ROWS - 1, -1, -1):
        if board[row_num][col_num] == ' ':
            board[row_num][col_num] = get_player_checker(player_num)
            return

def check_win(board, player_num):
    """Check for a win (horizontally, vertically, diagonally)"""
    checker = get_player_checker(player_num)
    # Check horizontal
    for row in board:
        for col in range(NUM_COLS - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True
    # Check vertical
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

def check_draw(board):
    """Check if the board is full (draw)"""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    board = create_board()
    print_board(board)
    players = list(range(1, NUM_PLAYERS + 1))
    random.shuffle(players)
    current_player = 0
    while True:
        player_num = players[current_player]
        input_str = input(f"Player {get_player_checker(player_num)}, please enter a column: ")
        if not is_valid_input(input_str):
            print("Invalid input. Please enter a column letter (A-G).")
            continue
        col_num = get_column_num(input_str)
        if is_column_full(board, col_num):
            print("Column is full. Please choose another column.")
            continue
        place_checker(board, player_num, col_num)
        print_board(board)
        if check_win(board, player_num):
            print(f"Player {get_player_checker(player_num)} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
