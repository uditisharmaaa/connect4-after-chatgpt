import os
import random

# Constants for board size and number of players
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2

# Player symbols
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print the column headers
    headers = '  ' + '   '.join(chr(65 + i) for i in range(COLUMNS))
    print(headers)
    print('+---' * COLUMNS + '+')
    # Print each row
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def get_valid_column_input(board):
    while True:
        column = input("Please enter a column (A-G): ").upper()
        if len(column) == 1 and 'A' <= column <= 'G':
            column_index = ord(column) - ord('A')
            if board[0][column_index] == ' ':
                return column_index
        print("Invalid input, please try again.")

def place_checker(board, column, player_symbol):
    for row_index in reversed(range(ROWS)):
        if board[row_index][column] == ' ':
            board[row_index][column] = player_symbol
            return

def check_win(board, player_symbol):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == player_symbol for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == player_symbol for i in range(4)):
                return True

    # Positive diagonal check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == player_symbol for i in range(4)):
                return True

    # Negative diagonal check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == player_symbol for i in range(4)):
                return True
                
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    board = create_board()
    current_player = random.choice(range(PLAYER_COUNT))
    
    print_board(board)
  
    while True:
        print(f"Player {PLAYER_SYMBOLS[current_player]}, it's your turn.")
        column = get_valid_column_input(board)
        place_checker(board, column, PLAYER_SYMBOLS[current_player])
        print_board(board)
        
        if check_win(board, PLAYER_SYMBOLS[current_player]):
            print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Alternate player
        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == "__main__":
    play_game()
