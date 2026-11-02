import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
MAX_PLAYERS = 5
PLAYERS_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """
    Creates the game board with specified dimensions and initializes it with whitespaces.
    """
    board = []
    for _ in range(BOARD_ROWS):
        row = []
        for _ in range(BOARD_COLUMNS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board):
    """
    Prints the current state of the game board.
    """
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| {} | {} | {} | {} | {} | {} | {} |'.format(*row))
    print('+---+---+---+---+---+---+---+')

def validate_input(player, column):
    """
    Checks if the player's input is valid.
    """
    if not column.isalpha():
        print('Invalid input. Please enter a letter.')
        return False
    column = ord(column.upper()) - 65
    if column < 0 or column >= BOARD_COLUMNS:
        print('Invalid input. Please enter a letter within the board.')
        return False
    return True

def place_checker(board, player, column):
    """
    Places the player's checker in the specified column.
    """
    column = ord(column.upper()) - 65
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = PLAYERS_CHECKERS[player]
            return

def check_win(board, player):
    """
    Checks if the player has won the game.
    """
    checker = PLAYERS_CHECKERS[player]
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == checker and row[i + 1] == checker and row[i + 2] == checker and row[i + 3] == checker:
                return True
    # Check vertical
    for col in range(BOARD_COLUMNS):
        for i in range(len(board) - 3):
            if board[i][col] == checker and board[i + 1][col] == checker and board[i + 2][col] == checker and board[i + 3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

def check_draw(board):
    """
    Checks if the game is a draw.
    """
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    num_players = 2
    players = list(range(num_players))
    random.shuffle(players)
    board = create_board()
    print_board(board)
    while True:
        for player in players:
            print('Player', PLAYERS_CHECKERS[player], 'please enter a column:')
            while True:
                column = input().strip()
                if validate_input(player, column):
                    break
            place_checker(board, player, column)
            print_board(board)
            if check_win(board, player):
                print('Player', PLAYERS_CHECKERS[player], 'won!')
                return
            if check_draw(board):
                print('It\'s a draw!')
                return

if __name__ == '__main__':
    main()
