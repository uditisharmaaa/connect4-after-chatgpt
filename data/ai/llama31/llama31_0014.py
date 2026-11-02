import os
import random
import string

# Constant variables
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Create the board
def create_board(width, height):
    return [[' ' for _ in range(width)] for _ in range(height)]

# Print the board
def print_board(board):
    columns = string.ascii_uppercase[:BOARD_WIDTH]
    print('  ' + '   '.join(columns))
    print('+---' * BOARD_WIDTH + '+')
    for row in board:
        print('|   ' * BOARD_WIDTH + '|')
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_WIDTH + '+')

# Check for a win
def check_win(board, player):
    # Check horizontal wins
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == row[col+1] == row[col+2] == row[col+3] == player:
                return True

    # Check vertical wins
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == player:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == player:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == player:
                return True

    return False

# Main game loop
def game():
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-{string.ascii_uppercase[BOARD_WIDTH-1]}): ")

        while True:
            try:
                column = input().strip().upper()
                if column not in string.ascii_uppercase[:BOARD_WIDTH]:
                    raise ValueError
                column = string.ascii_uppercase.index(column)
                break
            except ValueError:
                print("Invalid input. Please enter a letter between A and", string.ascii_uppercase[BOARD_WIDTH-1])

        for row in range(len(board) - 1, -1, -1):
            if board[row][column] == ' ':
                board[row][column] = current_player
                break
        else:
            print("Column is full. Please try again.")
            continue

        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if all(cell!= ' ' for row in board for cell in row):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

game()
