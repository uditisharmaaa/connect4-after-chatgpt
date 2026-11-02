import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change this to the number of players you want (up to 5)
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5"

def init_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print(' A B C D E F G')
    print('+---------------+')
    for row in board:
        print('|' + '|'.join(row) + '|')
        print('+---------------+')

def make_move(board, col, player_symbol):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player_symbol
            return True
    return False

def is_valid_column(col):
    return 0 <= col < COLS

def is_column_full(board, col):
    return board[0][col] != ' '

def check_winner(board, player_symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player_symbol for i in range(4)):
                return True
                
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True
                
    # Check diagonals (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True
                
    # Check diagonals (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True
                
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def get_player_column_choice(current_player):
    while True:
        choice = input(f"Player {current_player + 1}, choose a column (A-G): ").upper()
        if choice in 'ABCDEFG' and len(choice) == 1:
            return ord(choice) - ord('A')
        else:
            print("Invalid column. Please choose a column from A to G.")

def main():
    board = init_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        col = get_player_column_choice(current_player)

        if is_valid_column(col) and not is_column_full(board, col):
            make_move(board, col, PLAYER_SYMBOLS[current_player])
            print_board(board)

            if check_winner(board, PLAYER_SYMBOLS[current_player]):
                print(f"Player {current_player + 1} ({PLAYER_SYMBOLS[current_player]}) wins!")
                break

            if check_draw(board):
                print("The game is a draw!")
                break

            current_player = (current_player + 1) % NUM_PLAYERS
        else:
            print("Column is full or invalid. Try again!")
        
if __name__ == "__main__":
    main()
