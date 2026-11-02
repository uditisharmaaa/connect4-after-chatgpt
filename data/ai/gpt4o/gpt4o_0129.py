import os
import random

# Constant variables for game settings
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a 2D game board with all positions initialized to ' '"""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the game board to the console"""
    os.system('clear')
    column_labels = ' '.join([chr(65 + i) for i in range(NUM_COLS)])
    print('  ' + '   '.join(column_labels))
    print('+---' * NUM_COLS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * NUM_COLS + '+')

def is_valid_input(input_str):
    """Check if the input is a valid column letter"""
    if len(input_str) != 1:
        return False
    if not input_str.isalpha() or not input_str.isupper():
        return False
    if ord(input_str) - 65 >= NUM_COLS:
        return False
    return True

def get_next_open_row(board, col):
    """Return the next open row in the given column"""
    for row in range(NUM_ROWS-1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

def check_for_win(board, current_checker):
    """Check if the current player has won"""
    # Horizontal Check
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col:col + 4] == [current_checker] * 4:
                return True

    # Vertical Check
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if all(board[row + i][col] == current_checker for i in range(4)):
                return True

    # Diagonal Check (bottom left to top right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row + i][col + i] == current_checker for i in range(4)):
                return True

    # Diagonal Check (top left to bottom right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row - i][col + i] == current_checker for i in range(4)):
                return True

    return False

def is_board_full(board):
    """Check if the board is completely filled"""
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player_index]
    
    print_board(board)
    
    while True:
        print(f"Player {current_checker}, please enter a column:")
        while True:
            column_choice = input().upper()
            if is_valid_input(column_choice):
                col = ord(column_choice) - 65
                row = get_next_open_row(board, col)
                if row is not None:
                    break
                else:
                    print("Column is full! Choose another column.")
            else:
                print("Invalid input! Please enter a valid column letter.")
        
        board[row][col] = current_checker
        
        print_board(board)
        
        if check_for_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if is_board_full(board):
            print("Game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_checker = CHECKERS[current_player_index]

if __name__ == "__main__":
    main()
