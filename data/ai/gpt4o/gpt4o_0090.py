import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for players

# Board creation
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print board
def print_board(board):
    os.system('clear')  # Clears the screen
    print('  ' + '  '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

# Check for win
def check_win(board, player):
    def four_in_a_row(lst):
        return any(lst[i:i+4] == [player]*4 for i in range(len(lst) - 3))

    # Horizontal check
    for row in board:
        if four_in_a_row(row):
            return True

    # Vertical check
    for col in range(COLUMNS):
        if four_in_a_row([board[row][col] for row in range(ROWS)]):
            return True

    # Diagonal checks
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (
                row <= ROWS - 4 and
                col <= COLUMNS - 4 and
                all(board[row+i][col+i] == player for i in range(4))
            ):
                return True
            if (
                row >= 3 and
                col <= COLUMNS - 4 and
                all(board[row-i][col+i] == player for i in range(4))
            ):
                return True

    return False

# Check for draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Validate input
def validate_input(column_input):
    if column_input.isalpha():
        col = ord(column_input.upper()) - 65
        if 0 <= col < COLUMNS:
            return col
    return None

# Place checker
def place_checker(board, col, player):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def connect_4():
    board = create_board()
    num_players = 2  # Can be adjusted for more players
    players = CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    
    print_board(board)

    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        column_input = input().strip()
        
        col = validate_input(column_input)
        if col is None:
            print("Invalid input. Try again.")
            continue

        if place_checker(board, col, current_player):
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("It's a draw!")
                break

            # Alternate player
            current_player_index = (current_player_index + 1) % num_players
        else:
            print(f"Column {chr(65 + col)} is full. Turn lost.")

if __name__ == "__main__":
    connect_4()
