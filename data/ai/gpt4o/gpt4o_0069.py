import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLUMNS + '+')

def is_valid_move(board, column):
    if column < 0 or column >= COLUMNS:
        return False
    return board[0][column] == ' '

def make_move(board, column, checker):
    for row in reversed(range(ROWS)):
        if board[row][column] == ' ':
            board[row][column] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal, vertical, and diagonal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
            if all(board[row + 3 - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:", end=' ')
        move = input().strip().upper()
        column = ord(move) - 65

        if not is_valid_move(board, column):
            print("Invalid move. Try again.")
            continue

        if make_move(board, column, CHECKERS[current_player]):
            print_board(board)
            if check_winner(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            if is_draw(board):
                print("The game is a draw!")
                break

            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
