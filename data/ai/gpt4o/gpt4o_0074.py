import os
import random

# Constants for the board size and number of players
NUM_ROWS = 6
NUM_COLUMNS = 7
NUM_PLAYERS = 2

# Available checkers for players
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board with spaces
def create_board():
    return [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

# Print the board on the console
def print_board(board):
    os.system('clear')  # Clear the screen before printing
    print('  ' + '   '.join(chr(65 + i) for i in range(NUM_COLUMNS)))
    print('+' + '---+' * NUM_COLUMNS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * NUM_COLUMNS)

# Validate user input for column selection
def validate_input(column):
    if column.isalpha() and len(column) == 1:
        col_idx = ord(column.upper()) - 65
        return 0 <= col_idx < NUM_COLUMNS
    return False

# Place the checker in the correct position
def place_checker(board, column, player):
    column_index = ord(column.upper()) - 65
    if board[0][column_index] != ' ': # If column is full
        return False
    for row in reversed(range(NUM_ROWS)):
        if board[row][column_index] == ' ':
            board[row][column_index] = player
            break
    return True

# Check if there is a win condition
def check_win(board, player):
    # Check horizontal, vertical and diagonal conditions for win
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
            if all(board[row + 3 - i][col + i] == player for i in range(4)):
                return True
    return False

# Check if the game is a draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(NUM_COLUMNS))

# Main game loop
def main():
    board = create_board()
    players_in_game = PLAYERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_player = players_in_game[current_player_index]
        column = input(f'Player {current_player}, please enter a column: ')
        
        if not validate_input(column):
            print("Invalid input. Please enter a valid column letter.")
            continue

        if not place_checker(board, column, current_player):
            print("Column is full. You lose your turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS  # Change turn
            continue

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
