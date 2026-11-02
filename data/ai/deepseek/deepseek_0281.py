import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    # Print top border
    print('+' + ('---+' * COLS))
    
    for row in board:
        # Print row content
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        # Print border after each row
        print('+' + ('---+' * COLS))

def is_valid_column(col):
    return col >= 0 and col < COLS

def get_user_input(current_player):
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        col = ord(user_input) - ord('A')
        if not is_valid_column(col):
            print("Invalid column. Please choose a column from A to G.")
            continue
        return col

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(CHECKERS)
    clear_screen()
    print_board(board)
    
    while True:
        col = get_user_input(current_player)
        if not place_checker(board, col, current_player):
            print("Column is full. You lose your turn.")
            continue
        
        clear_screen()
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
