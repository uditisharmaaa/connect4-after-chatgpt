import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with whitespaces"""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with columns labeled by letters"""
    print('  ' + ' '.join(string.ascii_uppercase[:COLS]))
    print('+---' * COLS + '+')
    for row in board:
        print('|   ' * COLS + '|')
        print('| ' + ' | '.join(row) + ' |')
        print('|---' * COLS + '|')
    print()

def is_valid_input(input_str, cols):
    """Check if the input is a valid column letter"""
    return input_str in string.ascii_uppercase[:cols]

def get_player_input(player, board):
    """Get a valid column input from the player"""
    while True:
        input_str = input(f'Player {player}, please enter a column: ').strip().upper()
        if is_valid_input(input_str, COLS):
            return ord(input_str) - ord('A')
        print('Invalid input. Please try again.')

def place_checker(board, col, player):
    """Place a checker in the specified column"""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return
    print('Column is full. Try again.')

def check_win(board, player):
    """Check if the player has won"""
    # Check horizontal wins
    for row in board:
        for i in range(COLS - 3):
            if all(cell == player for cell in row[i:i+4]):
                return True

    # Check vertical wins
    for col in range(COLS):
        for i in range(ROWS - 3):
            if all(board[row][col] == player for row in range(i, i+4)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full (draw)"""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board)
        col = get_player_input(current_player, board)
        place_checker(board, col, current_player)

        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f'Player {current_player} won!')
            break

        if check_draw(board):
            os.system('clear')
            print_board(board)
            print('It\'s a draw!')
            break

        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == '__main__':
    main()
