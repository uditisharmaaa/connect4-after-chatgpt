import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    header = '  ' + '   '.join(chr(i + 65) for i in range(COLUMNS))
    print(header)
    print('+---' * COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLUMNS + '+')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def check_win(board, symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True
    
    # Check diagonal (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True
    
    # Check diagonal (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True
    
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def drop_checker(board, column, symbol):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = symbol
            return True
    return False

def validate_input(input_str):
    if len(input_str) == 1 and 'A' <= input_str <= 'G':
        return ord(input_str) - 65  # Convert column label to index
    return None

def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)
    print(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column:")

    while True:
        column_input = input().strip()
        column_index = validate_input(column_input)

        if column_index is not None:
            if drop_checker(board, column_index, PLAYER_SYMBOLS[current_player]):
                print_board(board)

                if check_win(board, PLAYER_SYMBOLS[current_player]):
                    print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
                    break
                
                if check_draw(board):
                    print("The game is a draw!")
                    break
                
                current_player = (current_player + 1) % PLAYERS
                print(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column:")
            else:
                print("Column is full. Turn is invalid.")
        else:
            print("Invalid input. Please enter a valid column:")
        
if __name__ == '__main__':
    play_game()
