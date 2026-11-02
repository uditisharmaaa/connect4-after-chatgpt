import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    print("+---" * COLS + "+")
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print("+---" * COLS + "+")

def get_column_index(col_char):
    return ord(col_char.upper()) - ord('A')

def is_valid_input(input_value):
    if len(input_value) != 1:
        return False
    col = get_column_index(input_value)
    return 0 <= col < COLS

def is_column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            break

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS-3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS-3):
        for col in range(COLS):
            if all(board[row+i][col] == checker for i in range(4)):
                return True
    # Check diagonal (down-right)
    for row in range(ROWS-3):
        for col in range(COLS-3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS-3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = create_board()
    print_board(board)

    current_player = random.randint(0, PLAYERS - 1)

    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        
        while True:
            user_input = input().strip()
            if not is_valid_input(user_input):
                print("Invalid input. Try again.")
            else:
                col = get_column_index(user_input)
                if is_column_full(board, col):
                    print("Column full. Try again.")
                else:
                    break
            
        place_checker(board, col, checker)
        print_board(board)

        if check_winner(board, checker):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
