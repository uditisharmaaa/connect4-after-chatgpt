import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column headers
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)]) + '  '
    print(header)
    
    # Print top border
    border = '+' + ('---+' * COLS)
    print(border)
    
    # Print each row
    for row in board:
        row_str = '|' + '|'.join([f' {cell} ' for cell in row]) + '|'
        print(row_str)
        print(border)

def is_valid_column(col):
    if len(col) != 1:
        return False
    col = col.upper()
    return 'A' <= col <= chr(65 + COLS - 1)

def get_column_index(col):
    return ord(col.upper()) - 65

def get_next_open_row(board, col_index):
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == ' ':
            return row
    return -1

def drop_checker(board, row, col, checker):
    board[row][col] = checker

def check_win(board, row, col, checker):
    # Check horizontal
    for c in range(COLS - 3):
        if all(board[row][c + i] == checker for i in range(4)):
            return True
    
    # Check vertical
    for r in range(ROWS - 3):
        if all(board[r + i][col] == checker for i in range(4)):
            return True
    
    # Check diagonal (positive slope)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (negative slope)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    
    return False

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = create_board()
    current_player = random.choice(range(NUM_PLAYERS))
    
    while True:
        clear_screen()
        print_board(board)
        
        player_checker = PLAYERS[current_player]
        print(f"Player {player_checker}, please enter a column: ")
        col_input = input().strip()
        
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column letter (A to G).")
            input("Press Enter to continue...")
            continue
        
        col_index = get_column_index(col_input)
        row = get_next_open_row(board, col_index)
        
        if row == -1:
            print("Column is full. You lose your turn.")
            input("Press Enter to continue...")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        drop_checker(board, row, col_index, player_checker)
        
        if check_win(board, row, col_index, player_checker):
            clear_screen()
            print_board(board)
            print(f"Player {player_checker} won!")
            break
        
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
