import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']
# Adjust PLAYERS list based on the current game configuration
CURRENT_PLAYERS = PLAYERS[:2]  # Change the slice based on the number of players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    print('  ' + '   '.join(chr(i + ord('A')) for i in range(COLS)))
    # Print board
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

def is_valid_input(input_value):
    return len(input_value) == 1 and 'A' <= input_value <= chr(ord('A') + COLS - 1)

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None  # Column is full

def drop_checker(board, row, col, checker):
    board[row][col] = checker

def is_winning_move(board, checker):
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    current_player_idx = random.randint(0, len(CURRENT_PLAYERS) - 1)
    game_over = False

    print_board(board)

    while not game_over:
        current_player = CURRENT_PLAYERS[current_player_idx]
        col_input = input(f"Player {current_player}, please enter a column: ")

        if not is_valid_input(col_input):
            print("Invalid input, please enter a column between A and G.")
            continue

        col = ord(col_input) - ord('A')
        row = get_next_open_row(board, col)

        if row is None:
            print("Column is full, please select another column.")
            continue

        drop_checker(board, row, col, current_player)

        print_board(board)

        if is_winning_move(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif is_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % len(CURRENT_PLAYERS)

if __name__ == '__main__':
    main()
