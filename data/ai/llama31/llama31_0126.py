import os
import random
import string

# Constant global variables
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(width, height):
    """Creates a 2D board with the given width and height, initialized with whitespaces."""
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_board(board, width, height):
    """Prints the current state of the board."""
    os.system('clear')
    column_labels = ' '.join(string.ascii_uppercase[:width])
    print(column_labels)
    for row in board:
        print('+---' * width + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * width + '+')

def is_valid_move(board, column):
    """Checks if a move is valid (i.e., the column is not full)."""
    return board[0][column] == ' '

def get_next_open_row(board, column):
    """Finds the next open row in the given column."""
    for row in range(BOARD_HEIGHT - 1, -1, -1):
        if board[row][column] == ' ':
            return row
    return -1  # column is full

def drop_checker(board, column, checker):
    """Drops a checker into the given column."""
    row = get_next_open_row(board, column)
    if row!= -1:
        board[row][column] = checker
        return True
    return False

def check_win(board, checker):
    """Checks for a win condition."""
    # Check horizontal locations for win
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(BOARD_WIDTH):
        for row in range(BOARD_HEIGHT - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def check_draw(board):
    """Checks if the game is a draw (i.e., the board is full)."""
    return all([cell!= ' ' for row in board for cell in row])

def main():
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    print_board(board, BOARD_WIDTH, BOARD_HEIGHT)
    while True:
        print(f"Player {current_player}, please enter a column:")
        column = input().upper()
        if column not in string.ascii_uppercase[:BOARD_WIDTH]:
            print("Invalid input. Please enter a column letter.")
            continue
        column_index = ord(column) - ord('A')
        if not is_valid_move(board, column_index):
            print("Column is full. Please choose another column.")
            continue
        if not drop_checker(board, column_index, current_player):
            print("Invalid move. Please try again.")
            continue
        print_board(board, BOARD_WIDTH, BOARD_HEIGHT)
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
