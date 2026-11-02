import os
import random

# Constants for board size and player count
BOARD_ROWS = 6
BOARD_COLUMNS = 7
PLAYER_COUNT = 2

# Symbols for players; More players can be added by extending this list
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    # Clear the terminal screen
    os.system('clear')

def create_board():
    # Create a board with specified dimensions initialized with whitespaces
    return [[' ' for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    # Print the board with column headers
    clear_screen()
    header = '  ' + '   '.join(chr(65 + i) for i in range(BOARD_COLUMNS))
    separator = '+---' * BOARD_COLUMNS + '+'
    print(header)
    print(separator)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print(separator)

def is_valid_move(column, board):
    # Check if the column is a valid move (within bounds and not full)
    if 0 <= column < BOARD_COLUMNS:
        return board[0][column] == ' '
    return False

def make_move(board, column, player_symbol):
    # Place the player's checker in the chosen column
    for row in reversed(range(BOARD_ROWS)):
        if board[row][column] == ' ':
            board[row][column] = player_symbol
            break

def check_winner(board, player_symbol):
    # Check horizontal, vertical and diagonal for a win
    # Horizontal check
    for row in board:
        for col in range(BOARD_COLUMNS - 3):
            if all(row[col + i] == player_symbol for i in range(4)):
                return True

    # Vertical check
    for col in range(BOARD_COLUMNS):
        for row in range(BOARD_ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True

    # Positive diagonal check
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True

    # Negative diagonal check
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    # Check if the board is full and no winner, resulting in a draw
    return all(board[0][col] != ' ' for col in range(BOARD_COLUMNS))

def play_game():
    board = create_board()
    current_player_index = random.randint(0, PLAYER_COUNT - 1)  # Select random starting player
    while True:
        print_board(board)
        current_player_symbol = PLAYER_SYMBOLS[current_player_index]
        print(f"Player {current_player_symbol}, please enter a column:")
        
        while True:
            user_input = input().strip().upper()
            if len(user_input) == 1 and 'A' <= user_input <= chr(65 + BOARD_COLUMNS - 1):
                column = ord(user_input) - 65
                if is_valid_move(column, board):
                    make_move(board, column, current_player_symbol)
                    break
                else:
                    print("Column is full. Choose another one:")
            else:
                print("Invalid input. Enter a valid column letter:")

        if check_winner(board, current_player_symbol):
            print_board(board)
            print(f"Player {current_player_symbol} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Alternate players
        current_player_index = (current_player_index + 1) % PLAYER_COUNT

if __name__ == "__main__":
    play_game()
