import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D list representing the Connect 4 board."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board, players, current_player):
    """Print the current state of the board."""
    os.system('clear')
    print(' ' + '   '.join(chr(65 + i) for i in range(NUM_COLS)))
    print(' ' + '+---' * NUM_COLS + '+')
    for row in board:
        print('|' + ' | '.join(row) + '|')
        print(' ' + '+---' * NUM_COLS + '+')
    print(f"Player {CHECKERS[current_player]}, please enter a column:")

def is_valid_input(column):
    """Check if the user's input is a valid column letter."""
    return 'A' <= column <= 'G'

def get_column_index(column):
    """Convert the column letter to a 0-based index."""
    return ord(column) - 65

def is_column_full(board, column):
    """Check if the specified column is full."""
    return board[0][column]!= ' '

def place_checker(board, column, checker):
    """Place the checker in the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(board, checker):
    """Check if the specified player has won."""
    # Check horizontal locations for win
    for row in board:
        for col in range(NUM_COLS - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def is_draw(board):
    """Check if the board is full and no player has won."""
    return all(all(cell!= ' ' for cell in row) for row in board)

def main():
    num_players = 2
    players = [i for i in range(num_players)]
    current_player = random.choice(players)
    board = create_board()

    while True:
        print_board(board, players, current_player)
        column = input().upper()
        if not is_valid_input(column):
            print("Invalid input. Please enter a column letter (A-G).")
            continue
        column_index = get_column_index(column)
        if is_column_full(board, column_index):
            print("Column is full. Please choose another column.")
            continue
        place_checker(board, column_index, CHECKERS[current_player])
        if check_win(board, CHECKERS[current_player]):
            print_board(board, players, current_player)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if is_draw(board):
            print_board(board, players, current_player)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
