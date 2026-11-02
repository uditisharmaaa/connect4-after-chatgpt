import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * COLS)

def get_valid_input(player):
    while True:
        try:
            col = input(f"Player {player}, please enter a column: ").upper()
            if len(col) != 1 or ord(col) < 65 or ord(col) >= 65 + COLS:
                raise ValueError("Invalid column. Please try again.")
            col_idx = ord(col) - 65
            return col_idx
        except ValueError as e:
            print(e)

def place_checker(board, col_idx, player):
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = player
            return True
    return False

def check_win(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board()
    current_player = random.choice(PLAYER_SYMBOLS)
    print_board(board)
    
    while True:
        col_idx = get_valid_input(current_player)
        if place_checker(board, col_idx, current_player):
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print("Draw!")
                break
            current_player = PLAYER_SYMBOLS[(PLAYER_SYMBOLS.index(current_player) + 1) % PLAYERS]
        else:
            print("Column is full. Try another column.")

if __name__ == "__main__":
    main()
