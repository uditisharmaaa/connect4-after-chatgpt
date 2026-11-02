import os
import random
import string

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(width, height):
    """
    Creates a 2D list filled with whitespaces to represent the board.
    """
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_board(board):
    """
    Prints the current state of the board.
    """
    print('  A B C D E F G')
    for row in board:
        print('+---' * BOARD_WIDTH + '+')
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
    print('+---' * BOARD_WIDTH + '+')

def get_player_input(player):
    """
    Asks the player for input and validates it.
    """
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if column in string.ascii_uppercase[:BOARD_WIDTH]:
            return column
        else:
            print("Invalid input. Please enter a letter from A to", string.ascii_uppercase[BOARD_WIDTH-1])

def place_checker(board, player, column):
    """
    Places a checker on the board at the specified column.
    """
    column_index = ord(column) - ord('A')
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = player
            return

def check_win(board, player):
    """
    Checks if the player has won.
    """
    # Check horizontal
    for row in board:
        for i in range(BOARD_WIDTH - 3):
            if row[i] == player and row[i+1] == player and row[i+2] == player and row[i+3] == player:
                return True

    # Check vertical
    for col in range(BOARD_WIDTH):
        for i in range(BOARD_HEIGHT - 3):
            if board[i][col] == player and board[i+1][col] == player and board[i+2][col] == player and board[i+3][col] == player:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
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
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board)
        column = get_player_input(current_player)
        place_checker(board, current_player, column)
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
