import os
import random

# Constants
NUM_ROWS = 6
NUM_COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COL_LABELS = [chr(ord('A') + i) for i in range(NUM_COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def print_board(board):
    header = '  ' + '   '.join(COL_LABELS)
    separator = '+---'*NUM_COLUMNS + '+'
    
    print(header)
    for row in board:
        print(separator)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(separator)

def get_random_player():
    return random.choice(range(NUM_PLAYERS))

def is_valid_input(input_str):
    return input_str in COL_LABELS

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[COL_LABELS.index(column)] == ' ':
            row[COL_LABELS.index(column)] = checker
            return True
    return False

def check_win(board, player_checker):
    # Check horizontal, vertical and diagonal for a win
    # Horizontal
    for row in board:
        for col in range(NUM_COLUMNS - 3):
            if all(row[col + i] == player_checker for i in range(4)):
                return True
                
    # Vertical
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if all(board[row + i][col] == player_checker for i in range(4)):
                return True
                
    # Diagonal /
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row - i][col + i] == player_checker for i in range(4)):
                return True
                
    # Diagonal \
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True
    
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = get_random_player()
    game_over = False

    while not game_over:
        clear_screen()
        print_board(board)
        current_checker = CHECKERS[current_player_index]
        player_input = ''
        
        while not is_valid_input(player_input):
            player_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        if place_checker(board, player_input, current_checker):
            if check_win(board, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                game_over = True
            elif check_draw(board):
                clear_screen()
                print_board(board)
                print("The game is a draw!")
                game_over = True
            else:
                current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
