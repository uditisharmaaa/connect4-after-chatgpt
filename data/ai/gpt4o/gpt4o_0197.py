import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(COLUMN_LABELS))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLUMNS + '+')

# Check for a win
def check_win(board, player):
    def check_direction(dy, dx):
        for y in range(ROWS):
            for x in range(COLUMNS):
                if all(0 <= y + i * dy < ROWS and
                       0 <= x + i * dx < COLUMNS and
                       board[y + i * dy][x + i * dx] == player
                       for i in range(4)):
                    return True
        return False
    
    return any(check_direction(dy, dx) for dy, dx in [(1, 0), (0, 1), (1, 1), (1, -1)])

# Check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Place a checker
def place_checker(board, column, player):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return True
    return False  # Column is full

# Main game loop
def play_game():
    board = create_board()
    current_player = random.choice(CHECKERS)
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        column_input = input().strip().upper()

        if column_input in COLUMN_LABELS:
            column_index = COLUMN_LABELS.index(column_input)

            if place_checker(board, column_index, current_player):
                print_board(board)

                if check_win(board, current_player):
                    print(f"Player {current_player} won!")
                    break

                if check_draw(board):
                    print("The game is a draw!")
                    break

                current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]
            else:
                print("Column is full. You lose your turn.")
        else:
            print("Invalid input. Try again.")

play_game()
