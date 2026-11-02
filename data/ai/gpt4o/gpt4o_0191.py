import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLUMNS))
    separator = '+---' * COLUMNS + '+'
    print(header)
    print(separator)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print(separator)

def is_valid_input(input_str, columns):
    if len(input_str) != 1:
        return False
    if not input_str.isalpha():
        return False
    col_index = ord(input_str.upper()) - ord('A')
    return 0 <= col_index < columns

def get_empty_row(board, col):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            return row
    return -1

def has_won(board, rows, columns, player):
    # Horizontal check
    for row in range(rows):
        for col in range(columns - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Vertical check
    for col in range(columns):
        for row in range(rows - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Diagonal check (/)
    for row in range(3, rows):
        for col in range(columns - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    # Diagonal check (\)
    for row in range(rows - 3):
        for col in range(columns - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board)
        current_player = CHECKERS[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        
        user_input = input().strip()
        if not is_valid_input(user_input, COLUMNS):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col = ord(user_input.upper()) - ord('A')
        row = get_empty_row(board, col)
        if row == -1:
            print("Column is full. You lose your turn.")
        else:
            board[row][col] = current_player
            if has_won(board, ROWS, COLUMNS, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
