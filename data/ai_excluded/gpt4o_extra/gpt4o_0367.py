import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
NUMBER_OF_PLAYERS = 2

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join([chr(65 + i) for i in range(COLUMNS)]))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLUMNS + '+')

def is_valid_move(board, col):
    return 0 <= col < COLUMNS and board[0][col] == ' '

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            return r
    return -1

def drop_checker(board, row, col, checker):
    board[row][col] = checker

def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS-3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Check vertical
    for r in range(ROWS-3):
        for c in range(COLUMNS):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Check positively sloped diagonals
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def get_player_input(player, checker):
    while True:
        col_input = input(f"Player {checker}, please enter a column: ")
        if len(col_input) == 1 and col_input.isalpha():
            col = ord(col_input.upper()) - 65
            if is_valid_move(board, col):
                return col
        print("Invalid input. Please try again.")

def switch_player(turn):
    return (turn + 1) % NUMBER_OF_PLAYERS

# Main game loop
def play_game():
    board = create_board()
    print_board(board)
    current_player = random.randint(0, NUMBER_OF_PLAYERS - 1)

    while True:
        checker = PLAYER_TOKENS[current_player]
        col = get_player_input(current_player, checker)
        row = get_next_open_row(board, col)
        drop_checker(board, row, col, checker)

        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = switch_player(current_player)

if __name__ == "__main__":
    play_game()
