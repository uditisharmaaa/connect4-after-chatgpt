import os
import random

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with the specified dimensions"""
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    print('  A B C D E F G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| {} | {} | {} | {} | {} | {} | {} |'.format(*row))
    print('+---+---+---+---+---+---+---+')

def validate_input(col):
    """Check if the input column is valid"""
    if not col.isalpha():
        return False
    if not 'A' <= col.upper() <= 'G':
        return False
    return True

def place_checker(board, col, checker):
    """Place a checker in the specified column"""
    col_index = ord(col.upper()) - ord('A')
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return

def check_win(board, checker):
    """Check if the current player has won"""
    # Check horizontal wins
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == checker and row[i+1] == checker and row[i+2] == checker and row[i+3] == checker:
                return True

    # Check vertical wins
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == checker and board[i+1][col] == checker and board[i+2][col] == checker and board[i+3][col] == checker:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    current_player = players[current_player_index]

    while True:
        os.system('clear')
        print_board(board)
        print("Player {}, please enter a column (A-G):".format(current_player))

        col = input().strip().upper()
        if not validate_input(col):
            print("Invalid input. Please enter a letter from A to G.")
            continue

        place_checker(board, col, current_player)

        if check_win(board, current_player):
            print("Player {} won!".format(current_player))
            break
        elif check_draw(board):
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS
        current_player = players[current_player_index]

if __name__ == "__main__":
    main()
