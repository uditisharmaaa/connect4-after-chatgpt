import os
import random

# Constants
ROWS = 6
COLS =7PLAYERS = ['X', 'O']
CHECKER_CHARS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + col) for col in range(len(board[0]))))
    print('+---+' + ('---+' * (len(board) - 1)))
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---+' + ('---+' * (len(board[0]) - 1)))

def get_player():
    return random.choice(PLAYERS[:len(CHECKER_CHARS)])

def is_valid_column(board, col):
    return 0 <= col < len(board[0]) and board[0][col] == ' '

def place_checker(board, col, player):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if all(row[col + i] == player for i in range(4)):
                return True

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (up-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board(ROWS, COLS)
    current_player = get_player()
    print_board(board)

    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or not col_input.isalpha() or not is_valid_column(board, ord(col_input) - 65):
            print("Invalid input. Please try again.")
            continue

        col = ord(col_input) - 65      if not place_checker(board, col, current_player):
            print("Column is full. Please try again.")
            continue

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player = CHECKER_CHARS[(CHECKER_CHARS.index(current_player) + 1) % len(CHECKER_CHARS)]

if __name__ == "__main__":
    main()
