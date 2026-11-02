import os
import random
import string

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']
LETTERS = string.ascii_uppercase

def create_board(width, height):
    """Create a 2D list representing the Connect 4 board."""
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + '   '.join(LETTERS[:BOARD_WIDTH]))
    print('+' + '+---' * BOARD_WIDTH + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '+---' * BOARD_WIDTH + '+')

def get_player_symbol(player):
    """Get the symbol for the current player."""
    return PLAYERS[player - 1]

def get_player_move(player, board):
    """Get the column number where the player wants to place their symbol."""
    while True:
        move = input(f"Player {get_player_symbol(player)}, please enter a column: ")
        if move in LETTERS[:BOARD_WIDTH]:
            return LETTERS.index(move)
        else:
            print("Invalid input. Please try again.")

def drop_symbol(board, column, symbol):
    """Drop the symbol in the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = symbol
            return

def check_win(board, symbol):
    """Check if the current player has won."""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == symbol for cell in row[i:i+4]]):
                return True

    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all([board[row][col] == symbol for row in range(i, i+4)]):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row+i][col+i] == symbol for i in range(4)]):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row-i][col+i] == symbol for i in range(4)]):
                return True

    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    return all([cell!= ' ' for row in board for cell in row])

def main():
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = list(range(1, NUM_PLAYERS + 1))
    random.shuffle(players)
    current_player = players[0]

    while True:
        print_board(board)
        column = get_player_move(current_player, board)
        symbol = get_player_symbol(current_player)
        drop_symbol(board, column, symbol)
        if check_win(board, symbol):
            print_board(board)
            print(f"Player {symbol} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
