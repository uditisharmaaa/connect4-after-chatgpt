import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

# Checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with ROWS x COLS dimensions"""
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    print('  ' + ' '.join(string.ascii_uppercase[:COLS]))
    print('+---' * COLS + '+')
    for row in board:
        print('|   ' * COLS + '|')
        print('+---' * COLS + '+')
    print()

def get_valid_input(prompt):
    """Get a valid input from the user"""
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) == 1 and user_input in string.ascii_uppercase[:COLS]:
            return user_input
        print("Invalid input. Please enter a column letter.")

def drop_checker(board, col, checker):
    """Drop a checker into the specified column"""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return

def check_win(board, checker):
    """Check if the specified checker has won"""
    # Check horizontal
    for row in board:
        for i in range(COLS - 3):
            if all(cell == checker for cell in row[i:i+4]):
                return True

    # Check vertical
    for col in range(COLS):
        for i in range(ROWS - 3):
            if all(board[row][col] == checker for row in range(i, i+4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    # Initialize the game
    board = create_board()
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player = random.choice(players)

    # Main game loop
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {current_player}, please enter a column:")

        # Get a valid input from the user
        col = string.ascii_uppercase.index(get_valid_input(''))

        # Drop the checker into the specified column
        drop_checker(board, col, current_player)

        # Check for a win or draw
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
