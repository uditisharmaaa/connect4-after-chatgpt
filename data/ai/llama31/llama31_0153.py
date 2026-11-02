import os
import random

# Constant global variables
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized with whitespaces."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
    print('+---+---+---+---+---+---+---+')

def get_player_checker(player_num):
    """Return the checker for the given player."""
    return CHECKERS[player_num - 1]

def is_valid_input(column):
    """Check if the input column is valid."""
    return 'A' <= column <= 'G' and column.isalpha()

def get_column_num(column):
    """Convert the column letter to a column number."""
    return ord(column.upper()) - ord('A')

def is_column_full(board, column):
    """Check if the given column is full."""
    return board[0][column]!= ' '

def place_checker(board, player_num, column):
    """Place the checker in the given column."""
    checker = get_player_checker(player_num)
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(board, player_num):
    """Check if the given player has won."""
    checker = get_player_checker(player_num)
    # Check horizontal
    for row in board:
        for i in range(NUM_COLS - 3):
            if all(row[i + j] == checker for j in range(4)):
                return True
    # Check vertical
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if all(board[i + j][col] == checker for j in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row + j][col + j] == checker for j in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row - j][col + j] == checker for j in range(4)):
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(all(cell!= ' ' for cell in row) for row in board)

def main():
    board = create_board()
    players = list(range(1, NUM_PLAYERS + 1))
    random.shuffle(players)
    current_player = players.pop(0)
    while True:
        print_board(board)
        print(f"Player {get_player_checker(current_player)}, please enter a column:")
        column = input().upper()
        while not is_valid_input(column) or is_column_full(board, get_column_num(column)):
            if not is_valid_input(column):
                print("Invalid input. Please enter a letter between A and G.")
            else:
                print("Column is full. Please choose another column.")
            column = input().upper()
        place_checker(board, current_player, get_column_num(column))
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {get_player_checker(current_player)} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players.pop(0)
        players.append(current_player)

if __name__ == "__main__":
    main()
