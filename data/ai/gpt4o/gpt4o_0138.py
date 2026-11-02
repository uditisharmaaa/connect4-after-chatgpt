import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS_COUNT = 2
PLAYERS_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # symbols for up to 5 players
COLUMN_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:COLUMNS]

def initialize_board(rows, columns):
    """Initialize the board with empty spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen before printing the board
    print('  ' + '   '.join(COLUMN_LETTERS[:COLUMNS]))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def get_column_input():
    """Get and validate user input for the column choice."""
    while True:
        column = input(f"Player {PLAYERS_SYMBOLS[current_player]}, please enter a column: ").upper()
        if column in COLUMN_LETTERS[:COLUMNS]:
            return COLUMN_LETTERS.index(column)
        else:
            print("Invalid input. Please enter a valid column letter.")

def place_checker(board, column, player_symbol):
    """Place the checker in the correct position in the chosen column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player_symbol
            return True
    return False  # Column is full

def check_winner(board, symbol):
    """Check if the current player has won the game."""
    # Check horizontal, vertical, and diagonal connections for a win
    for row in range(ROWS):
        for col in range(COLUMNS):
            if col <= COLUMNS - 4 and all(board[row][col + i] == symbol for i in range(4)):
                return True
            if row <= ROWS - 4 and all(board[row + i][col] == symbol for i in range(4)):
                return True
            if col <= COLUMNS - 4 and row <= ROWS - 4 and all(board[row + i][col + i] == symbol for i in range(4)):
                return True
            if col >= 3 and row <= ROWS - 4 and all(board[row + i][col - i] == symbol for i in range(4)):
                return True
    return False

def check_draw(board):
    """Check if the game is a draw (i.e., no empty spaces left)."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    global current_player
    board = initialize_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS_COUNT - 1)  # Randomly select the first player

    while True:
        print_board(board)
        column = get_column_input()
        if place_checker(board, column, PLAYERS_SYMBOLS[current_player]):
            if check_winner(board, PLAYERS_SYMBOLS[current_player]):
                print_board(board)
                print(f"Player {PLAYERS_SYMBOLS[current_player]} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % PLAYERS_COUNT
        else:
            print("Column is full. You lost your turn.")

if __name__ == '__main__':
    main()
