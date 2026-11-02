import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

# Checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a 2D board with whitespaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board with column labels."""
    print('  ' + ' '.join(string.ascii_uppercase[:COLS]))
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

def get_player_move(player, board):
    """Get the player's move and validate it."""
    while True:
        move = input(f'Player {player}, please enter a column: ').strip().upper()
        if move in string.ascii_uppercase[:COLS]:
            col = string.ascii_uppercase.index(move)
            if board[0][col]!= ' ':
                print("Column is already full. Please choose another column.")
            else:
                return col
        else:
            print("Invalid input. Please enter a column letter.")

def drop_checker(board, player, col):
    """Drop the checker into the column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return

def check_win(board, player):
    """Check if the player has won."""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == player and row[i+1] == player and row[i+2] == player and row[i+3] == player:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == player and board[i+1][col] == player and board[i+2][col] == player and board[i+3][col] == player:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    # Initialize the board
    board = create_board(ROWS, COLS)

    # Choose a random player to start
    current_player = random.choice(CHECKERS[:PLAYERS])

    while True:
        # Clear the screen
        os.system('clear')

        # Print the board
        print_board(board)

        # Get the player's move
        col = get_player_move(current_player, board)

        # Drop the checker
        drop_checker(board, current_player, col)

        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f'Player {current_player} won!')
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print('It\'s a draw!')
            break

        # Switch to the next player
        CHECKERS.index(current_player)
        current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]

if __name__ == '__main__':
    main()
