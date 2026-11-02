import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column labels
    print('  ', end='')
    for i in range(COLS):
        print(f'  {chr(65 + i)} ', end='')
    print()
    
    # Print rows
    for row in board:
        print('  +' + '---+' * COLS)
        print('  |', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
    print('  +' + '---+' * COLS)

def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == ' '

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    # Horizontal
    for c in range(COLS - 3):
        if all(board[row][c + i] == checker for i in range(4)):
            return True
    
    # Vertical
    for r in range(ROWS - 3):
        if all(board[r + i][col] == checker for i in range(4)):
            return True
    
    # Diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    
    # Diagonal (down-left)
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if all(board[r + i][c - i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def get_column_input(player):
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip()
        if len(col_input) == 1 and col_input.isalpha():
            col = ord(col_input.upper()) - 65
            if 0 <= col < COLS:
                return col
        print("Invalid input. Please try again.")

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_idx]
        
        col = get_column_input(current_checker)
        
        if not is_valid_move(board, col):
            print("Column is full. You lose your turn.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue
        
        row = place_checker(board, col, current_checker)
        print_board(board)
        
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
