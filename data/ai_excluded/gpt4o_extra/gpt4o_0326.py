import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    print('  ' + '   '.join([chr(i) for i in range(ord('A'), ord('A') + COLS)]))
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def get_column_number(char):
    return ord(char.upper()) - ord('A')

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def is_valid_column(col_choice):
    return col_choice.isalpha() and len(col_choice) == 1 and 'A' <= col_choice <= chr(ord('A') + COLS - 1)

def check_for_win(board, checker):
    # Check horizontally
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True
    # Check vertically
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonally (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonally (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    return False

def check_for_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def main():
    board = create_board(ROWS, COLS)
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player = random.choice(players)

    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column:")
        col_choice = input().strip()
        
        if not is_valid_column(col_choice):
            print("Invalid input, please enter a valid column.")
            continue
        
        col = get_column_number(col_choice)
        
        if not place_checker(board, col, current_player):
            print("Column is full, try another column.")
            continue
        
        print_board(board)
        
        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_for_draw(board):
            print("The game is a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
