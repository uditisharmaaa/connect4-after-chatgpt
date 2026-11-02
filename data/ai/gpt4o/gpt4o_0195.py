import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)]))
    print('+---' * COLS + '+')
    for row in board:
        print('|' + '|'.join([' {0} '.format(cell) for cell in row]) + '|')
        print('+---' * COLS + '+')

def get_valid_column():
    while True:
        col = input("Please enter a column (A-G): ").upper()
        if len(col) == 1 and col.isalpha() and ord(col) - ord('A') < COLS:
            return ord(col) - ord('A')
        else:
            print(f"Invalid column: {col}. Try again.")

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False  # Column is full

def check_for_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal checks (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Diagonal checks (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = initialize_board()
    print_board(board)

    current_player = random.randint(0, NUM_PLAYERS - 1)
    player_char = [CHECKERS[i] for i in range(NUM_PLAYERS)]

    while True:
        print_board(board)
        print(f"Player {player_char[current_player]}'s turn.")
        col = get_valid_column()

        if not place_checker(board, col, player_char[current_player]):
            print(f"Column {chr(ord('A') + col)} is full. You lose your turn.")
        else:
            if check_for_win(board, player_char[current_player]):
                print_board(board)
                print(f"Player {player_char[current_player]} won!")
                break
            if check_for_draw(board):
                print_board(board)
                print("It's a draw!")
                break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
