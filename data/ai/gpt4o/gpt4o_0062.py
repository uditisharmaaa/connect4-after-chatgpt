import random
import os

# Constants
NUM_ROWS = 6
NUM_COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Player identifiers

# Initialize the game board
board = [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def print_board():
    os.system('clear')
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(NUM_COLUMNS)]))
    print('+' + '---+' * NUM_COLUMNS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * NUM_COLUMNS)

def is_valid_column(column):
    return column.isalpha() and ord(column) - ord('A') < NUM_COLUMNS

def is_column_full(column_index):
    return board[0][column_index] != ' '

def drop_checker(column_index, player):
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = player
            return

def check_winner(player):
    # Check horizontal, vertical, diagonal (both directions)
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row][c] == player for c in range(col, col + 4)):
                return True

    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if all(board[r][col] == player for r in range(row, row + 4)):
                return True

    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row + d][col + d] == player for d in range(4)):
                return True

    for row in range(NUM_ROWS - 3):
        for col in range(3, NUM_COLUMNS):
            if all(board[row + d][col - d] == player for d in range(4)):
                return True

    return False

def check_draw():
    return all(board[0][col] != ' ' for col in range(NUM_COLUMNS))

def main():
    num_players = 2  # Set the number of players
    players = PLAYERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    while True:
        print_board()
        current_player = players[current_player_index]
        column = input(f"Player {current_player}, please enter a column: ")

        if not is_valid_column(column):
            print("Invalid input. Please choose a column between A and G.")
            continue

        column_index = ord(column) - ord('A')
        if is_column_full(column_index):
            print("Column is full. You lost the turn.")
            current_player_index = (current_player_index + 1) % num_players
            continue

        drop_checker(column_index, current_player)

        if check_winner(current_player):
            print_board()
            print(f"Player {current_player} won!")
            break

        if check_draw():
            print_board()
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == '__main__':
    main()
