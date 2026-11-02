import os
import random
import string

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(width, height):
    """Create a new board with the given width and height."""
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_WIDTH]))
    print('+---' * BOARD_WIDTH + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_WIDTH + '+')

def get_valid_move(player, board):
    """Get a valid move from the player."""
    while True:
        move = input(f"Player {CHECKERS[player]}, please enter a column: ")
        if move in string.ascii_uppercase[:BOARD_WIDTH]:
            column = string.ascii_uppercase.index(move)
            if ' ' in [row[column] for row in board]:
                return column
            else:
                print("Column is full, please choose another column.")
        else:
            print("Invalid input, please enter a letter between A and G.")

def drop_checker(board, column, checker):
    """Drop a checker into the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(board, checker):
    """Check if the given player has won."""
    # Check horizontal locations for win
    for row in board:
        for col in range(BOARD_WIDTH - 3):
            if row[col] == checker and row[col+1] == checker and row[col+2] == checker and row[col+3] == checker:
                return True

    # Check vertical locations for win
    for col in range(BOARD_WIDTH):
        for row in range(BOARD_HEIGHT - 3):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw."""
    return all([cell!= ' ' for row in board for cell in row])

def main():
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player = 0

    while True:
        print_board(board)
        column = get_valid_move(players[current_player], board)
        drop_checker(board, column, CHECKERS[players[current_player]])
        if check_win(board, CHECKERS[players[current_player]]):
            print_board(board)
            print(f"Player {CHECKERS[players[current_player]]} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
