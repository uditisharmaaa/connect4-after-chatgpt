import os
import random

# Constant global variables
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with whitespaces"""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print('  A B C D E F G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| {} | {} | {} | {} | {} | {} | {} |'.format(*row))
    print('+---+---+---+---+---+---+---+')

def get_valid_input(player, board):
    """Get a valid column input from the player"""
    while True:
        col = input("Player {}, please enter a column: ".format(player)).upper()
        if col < 'A' or col > 'G':
            print("Invalid input. Please enter a letter between A and G.")
        elif board[NUM_ROWS-1][ord(col)-ord('A')]!= ' ':
            print("Column is full. Please choose another column.")
        else:
            return ord(col)-ord('A')

def drop_checker(board, col, player):
    """Drop the checker into the specified column"""
    for row in range(NUM_ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = CHECKERS[player-1]
            return

def check_win(board, player):
    """Check if the player has won"""
    checker = CHECKERS[player-1]
    # Check horizontal locations for win
    for c in range(NUM_COLS-3):
        for r in range(NUM_ROWS):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # Check vertical locations for win
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # Check positively sloped diagonals
    for c in range(NUM_COLS-3):
        for r in range(NUM_ROWS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # Check negatively sloped diagonals
    for c in range(NUM_COLS-3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw"""
    return all([all([cell!= ' ' for cell in row]) for row in board])

def main():
    board = create_board()
    players = list(range(1, NUM_PLAYERS+1))
    random.shuffle(players)
    while True:
        for player in players:
            print_board(board)
            col = get_valid_input(player, board)
            drop_checker(board, col, player)
            if check_win(board, player):
                print_board(board)
                print("Player {} won!".format(player))
                return
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                return

if __name__ == "__main__":
    main()
