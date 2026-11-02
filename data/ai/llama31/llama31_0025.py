import os
import random
import string

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board"""
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:NUM_COLS]))
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * NUM_COLS + '+')

def validate_input(input_str, num_cols):
    """Check if input is a valid column letter"""
    return input_str in string.ascii_uppercase[:num_cols]

def get_player_checker(player_num):
    """Get the checker for the current player"""
    return CHECKERS[player_num - 1]

def drop_checker(board, column, checker):
    """Drop a checker in the specified column"""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(board, checker):
    """Check if the current player has won"""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == checker for cell in row[i:i+4]]):
                return True

    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all([board[row][col] == checker for row in range(i, i+4)]):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row+i][col+i] == checker for i in range(4)]):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row-i][col+i] == checker for i in range(4)]):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    return all([all([cell!= ' ' for cell in row]) for row in board])

def main():
    board = create_board()
    players = list(range(1, NUM_PLAYERS + 1))
    random.shuffle(players)

    while True:
        for player in players:
            print_board(board)
            input_str = input(f"Player {get_player_checker(player)}, please enter a column: ")
            if validate_input(input_str, NUM_COLS):
                column = string.ascii_uppercase.index(input_str)
                drop_checker(board, column, get_player_checker(player))
                if check_win(board, get_player_checker(player)):
                    print_board(board)
                    print(f"Player {get_player_checker(player)} won!")
                    return
                if check_draw(board):
                    print_board(board)
                    print("It's a draw!")
                    return
            else:
                print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
