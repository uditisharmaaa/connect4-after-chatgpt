import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '   |' * COLS)
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print('+' + '---+' * COLS)

def validate_input(input_str, board):
    if len(input_str) != 1 or not input_str.isalpha():
        return False
    col = ord(input_str.upper()) - 65
    return 0 <= col < COLS and board[0][col] == ' '

def place_checker(board, col, symbol):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = symbol
            break

def check_for_win(board, symbol):
    def check_line(line):
        return any(line[i:i+4] == [symbol]*4 for i in range(len(line) - 3))
    
    # Check rows for win
    for row in board:
        if check_line(row):
            return True
    
    # Check columns for win
    for col in range(COLS):
        if check_line([board[row][col] for row in range(ROWS)]):
            return True
    
    # Check diagonals for win
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == symbol for i in range(4)):
                return True
            if all(board[row+i][col+3-i] == symbol for i in range(4)):
                return True
    
    return False

def check_for_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_symbol = PLAYER_SYMBOLS[current_player_index]
    
    print_board(board)
    
    while True:
        user_input = ''
        while not validate_input(user_input, board):
            user_input = input(f"Player {current_symbol}, please enter a column: ")
        
        col = ord(user_input.upper()) - 65
        place_checker(board, col, current_symbol)
        
        print_board(board)
        
        if check_for_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break
        elif check_for_draw(board):
            print("The game is a draw!")
            break
        
        # Alternate player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_symbol = PLAYER_SYMBOLS[current_player_index]

if __name__ == "__main__":
    main()
