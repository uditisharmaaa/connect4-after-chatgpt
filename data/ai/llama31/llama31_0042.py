import os
import random

# Constant variables
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

def create_board():
    """Create a 2D board with all elements initialized to whitespaces."""
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  A', end='')
    for i in range(1, NUM_COLS):
        print(' ', chr(65 + i), end='')
    print()
    print('+---' * NUM_COLS + '+')
    for row in board:
        print('|', end='')
        for cell in row:
            print(' ' + cell + ' |', end='')
        print()
        print('+---' * NUM_COLS + '+')

def get_valid_input(player, board):
    """Get a valid column input from the player."""
    while True:
        col = input(f"Player {player}, please enter a column: ")
        if len(col)!= 1 or not col.isalpha() or ord(col) < 65 or ord(col) > 64 + NUM_COLS:
            print("Invalid input. Please enter a letter between A and", chr(65 + NUM_COLS - 1))
        elif all(cell!= ' ' for cell in board[0][ord(col) - 65]):
            print("Column is full. Please choose another column.")
        else:
            return ord(col) - 65

def place_checker(board, col, player):
    """Place a checker in the lowest available space in the given column."""
    for i in range(NUM_ROWS - 1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = player
            break

def check_win(board, player):
    """Check if the given player has won."""
    # Check horizontal
    for row in board:
        for i in range(NUM_COLS - 3):
            if row[i] == player and row[i + 1] == player and row[i + 2] == player and row[i + 3] == player:
                return True
    # Check vertical
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if board[i][col] == player and board[i + 1][col] == player and board[i + 2][col] == player and board[i + 3][col] == player:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    while True:
        print_board(board)
        col = get_valid_input(current_player, board)
        place_checker(board, col, current_player)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
