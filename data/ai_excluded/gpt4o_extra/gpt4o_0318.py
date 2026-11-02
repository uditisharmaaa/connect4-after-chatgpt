import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Player checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Create the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')
        
# Check if a column is valid and not full
def is_valid_column(column_input, board):
    if column_input.isalpha() and len(column_input) == 1:
        column = ord(column_input.upper()) - 65
        if 0 <= column < COLUMNS and board[0][column] == ' ':
            return True
    return False

# Place the checker in the chosen column
def place_checker(board, column, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return row, column

# Check for win in all directions
def check_winner(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Diagonal \ check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Diagonal / check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Main game loop
def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column_input = input().strip()

        if is_valid_column(column_input, board):
            column = ord(column_input.upper()) - 65
            place_checker(board, column, CHECKERS[current_player])

            if check_winner(board, CHECKERS[current_player]):
                print_board(board)
                print(f"Player {CHECKERS[current_player]} won!")
                break

            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

            current_player = (current_player + 1) % PLAYERS
            print_board(board)
        else:
            print("Invalid input, please enter a column (e.g., A, B, C).")

if __name__ == "__main__":
    play_game()
