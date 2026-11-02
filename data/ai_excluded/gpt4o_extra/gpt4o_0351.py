import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # For Linux/Unix
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+' + '---+' * COLUMNS)
    for row in board:
        print('|' + '   |' * COLUMNS)
        print('|' + ' '.join(row[i] for i in range(COLUMNS)) + ' |')
        print('|' + '   |' * COLUMNS)
        print('+' + '---+' * COLUMNS)

def is_valid_input(choice):
    return choice.isalpha() and ord(choice.upper()) - 65 < COLUMNS

def place_checker(board, col, checker):
    for i in range(ROWS-1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = checker
            return True
    return False

def check_for_win(board, checker):
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] == checker:
                return True
    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == checker:
                return True
    # Check diagonal (down-right) win
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True
    # Check diagonal (down-left) win
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3] == checker:
                return True
    return False

def check_for_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game():
    board = create_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    players = CHECKERS[:PLAYERS]
    game_over = False
    
    print_board(board)

    while not game_over:
        current_player = players[current_player_index]
        choice = input(f'Player {current_player}, please enter a column: ').upper()

        if not is_valid_input(choice):
            print("Invalid input, please enter a valid column letter.")
            continue

        selected_col = ord(choice) - 65

        if not place_checker(board, selected_col, current_player):
            print("Column is full, you lost your turn.")
        else:
            print_board(board)
            if check_for_win(board, current_player):
                print(f"Player {current_player} won!")
                game_over = True
            elif check_for_draw(board):
                print("Game is a draw!")
                game_over = True
            else:
                current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == '__main__':
    play_game()
