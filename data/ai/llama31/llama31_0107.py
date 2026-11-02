import os
import random
import string

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with whitespace elements"""
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board):
    """Print the board with column labels and row separators"""
    print('  ' + ' '.join(string.ascii_uppercase[:NUM_COLS]))
    print('+---' * NUM_COLS + '+')
    for row in board:
        print('|' + '|'.join([' ' + cell + ' ' for cell in row]) + '|')
        print('+---' * NUM_COLS + '+')

def validate_input(column):
    """Validate user input: must be an uppercase letter within the column range"""
    if len(column)!= 1 or not column.isalpha() or not column.isupper():
        return False
    return string.ascii_uppercase.index(column) < NUM_COLS

def place_checker(board, column, player):
    """Place a checker in the lowest available space in the specified column"""
    for row in reversed(board):
        if row[string.ascii_uppercase.index(column)] == ' ':
            row[string.ascii_uppercase.index(column)] = player
            return

def check_win(board, player):
    """Check if a player has won by finding 4 consecutive checkers"""
    # Check horizontal wins
    for row in board:
        for i in range(NUM_COLS - 3):
            if row[i] == player and row[i+1] == player and row[i+2] == player and row[i+3] == player:
                return True

    # Check vertical wins
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if board[i][col] == player and board[i+1][col] == player and board[i+2][col] == player and board[i+3][col] == player:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True

    return False

def check_draw(board):
    """Check if the board is full (i.e., a draw)"""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    # Create the board and print the initial state
    board = create_board()
    os.system('clear')
    print_board(board)

    # Randomly select the first player
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    players.remove(current_player)
    players.insert(0, current_player)

    while True:
        # Ask the current player for input
        column = input(f"Player {current_player}, please enter a column: ").strip()

        # Validate input
        while not validate_input(column):
            column = input("Invalid input. Please enter a column letter: ").strip()

        # Place the checker
        place_checker(board, column, current_player)

        # Check for a win
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % len(players)]

        # Clear the screen and print the updated board
        os.system('clear')
        print_board(board)

if __name__ == '__main__':
    main()
