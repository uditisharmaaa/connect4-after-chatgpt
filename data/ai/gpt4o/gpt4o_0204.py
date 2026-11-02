import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26
NUM_PLAYERS = 2
CHECKER_MARKS = ["X", "O", "V", "H", "M"]
CHECKERS = CHECKER_MARKS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns_labels = ' '.join(chr(ord('A') + i) for i in range(len(board[0])))
    print("  " + columns_labels)
    
    print('+' + ('---+' * len(board[0])))
    for row in board:
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print('+' + ('---+' * len(board[0])))

def make_move(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def is_valid_column(board, col_letter):
    col_index = ord(col_letter.upper()) - ord('A')
    if col_index < 0 or col_index >= len(board[0]) or board[0][col_index] != ' ':
        return False
    return True

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
                
    # Check vertical
    for col in range(cols):
        for row in range(rows - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
                
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    random_player = random.randint(0, NUM_PLAYERS - 1)
    current_player = random_player
    
    print_board(board)
    
    while True:
        current_checker = CHECKERS[current_player]
        print(f"Player {current_checker}, please enter a column:")
        
        while True:
            try:
                column_input = input().strip()
                if is_valid_column(board, column_input):
                    make_move(board, ord(column_input.upper()) - ord('A'), current_checker)
                    break
                else:
                    print("Invalid input. Please enter a valid column: ")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid column: ")
        
        print_board(board)
        
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
