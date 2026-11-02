import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    # Print top border
    print('+' + '---+' * COLS)
    # Print each row
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def is_valid_input(col_char):
    if len(col_char) != 1:
        return False
    col = ord(col_char.upper()) - ord('A')
    return 0 <= col < COLS

def place_checker(board, col_char, player):
    col = ord(col_char.upper()) - ord('A')
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_winner(board, player):
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
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        col_char = input(f"Player {current_player}, please enter a column: ").upper()
        
        if not is_valid_input(col_char):
            print("Invalid input. Please enter a valid column letter (A-{}).".format(chr(65 + COLS - 1)))
            continue
        
        if not place_checker(board, col_char, current_player):
            print("Column is full. Please choose another column.")
            continue
        
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game is a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
