import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with the given dimensions"""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| {} | {} | {} | {} | {} | {} | {} |'.format(*row))
    print('+---+---+---+---+---+---+---+')

def is_valid_input(col):
    """Check if the user input is a valid column"""
    return 'A' <= col <= 'G'

def get_col_from_input(input_str):
    """Convert the user input to a column index"""
    return ord(input_str) - ord('A')

def is_valid_move(board, col):
    """Check if the move is valid (i.e., the column is not full)"""
    return board[0][col] == ' '

def make_move(board, player, col):
    """Make a move on the board"""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            break

def check_win(board, player):
    """Check if the player has won"""
    # Check horizontal wins
    for row in board:
        for i in range(len(row) - 3):
            if all(cell == player for cell in row[i:i+4]):
                return True

    # Check vertical wins
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all(board[row][col] == player for row in range(i, i+4)):
                return True

    # Check diagonal wins
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True
            if all(board[row+i][col+3-i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board)
        print("Player {}, please enter a column:".format(current_player))

        while True:
            col_input = input().upper()
            if is_valid_input(col_input):
                col = get_col_from_input(col_input)
                if is_valid_move(board, col):
                    make_move(board, current_player, col)
                    break
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input, please enter a column letter.")

        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print("Player {} won!".format(current_player))
            break

        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % len(players)]

game()
