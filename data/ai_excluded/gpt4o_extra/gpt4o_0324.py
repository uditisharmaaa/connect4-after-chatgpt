import os
import random

# Constants for the game
NUM_ROWS = 6
NUM_COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players' symbols

def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(len(board[0]))))
    print('+' + '---+' * len(board[0]))
    # Print each row
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def get_column_input(num_columns):
    while True:
        column_input = input(f"Please enter a column (A-{chr(65 + num_columns - 1)}): ").upper()
        if len(column_input) == 1 and 'A' <= column_input <= chr(65 + num_columns - 1):
            return ord(column_input) - 65
        print("Invalid input. Please try again.")

def drop_checker(board, column, player):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return True
    return False

def check_winner(board, player):
    # Horizontal check
    for row in board:
        for col in range(NUM_COLUMNS - 3):
            if all(cell == player for cell in row[col:col + 4]):
                return True
    # Vertical check
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Diagonal (positive slope) check
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Diagonal (negative slope) check
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Game setup
    num_players = 2  # for this assignment submission
    board = initialize_board(NUM_ROWS, NUM_COLUMNS)
    current_player_index = random.randint(0, num_players - 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}'s turn")
        column = get_column_input(NUM_COLUMNS)

        if not drop_checker(board, column, current_player):
            print("Column full! You lose your turn.")
        else:
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print_board(board)
                print("It's a draw!")
                break
        
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
