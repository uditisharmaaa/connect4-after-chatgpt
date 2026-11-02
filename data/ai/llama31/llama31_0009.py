import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Function to create the board
def create_board(width, height):
    board = [[' ' for _ in range(width)] for _ in range(height)]
    return board

# Function to print the board
def print_board(board):
    print('  ' + ' '.join(chr(65+i) for i in range(len(board[0]))))
    for row in board:
        print('+---' * len(row) + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * len(board[0]) + '+')

# Function to validate player input
def validate_input(player, column):
    if not column.isalpha():
        return False
    column = ord(column.upper()) - 65
    if column < 0 or column >= BOARD_WIDTH:
        return False
    if board[0][column]!= ' ':
        return False
    return True

# Function to place a checker
def place_checker(board, player, column):
    for row in range(BOARD_HEIGHT-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player
            return

# Function to check for a win
def check_win(board, player):
    # Check horizontal locations for win
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH-3):
            if board[row][col] == player and board[row][col+1] == player and board[row][col+2] == player and board[row][col+3] == player:
                return True

    # Check vertical locations for win
    for col in range(BOARD_WIDTH):
        for row in range(BOARD_HEIGHT-3):
            if board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_HEIGHT-3):
        for col in range(BOARD_WIDTH-3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_HEIGHT):
        for col in range(BOARD_WIDTH-3):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True

    return False

# Function to check for a draw
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# Create the board
board = create_board(BOARD_WIDTH, BOARD_HEIGHT)

# Choose the first player randomly
first_player = random.randint(0, PLAYERS-1)
players = CHECKERS[:PLAYERS]

# Clear the screen and print the initial board
os.system('clear')
print_board(board)

# Game loop
current_player = first_player
while True:
    # Get the player's move
    while True:
        column = input(f'Player {players[current_player]}, please enter a column: ')
        if validate_input(players[current_player], column):
            break
        else:
            print('Invalid input, please try again.')

    # Place the checker
    place_checker(board, players[current_player], column)

    # Clear the screen and print the updated board
    os.system('clear')
    print_board(board)

    # Check for a win
    if check_win(board, players[current_player]):
        print(f'Player {players[current_player]} won!')
        break

    # Check for a draw
    if check_draw(board):
        print('It\'s a draw!')
        break

    # Switch to the next player
    current_player = (current_player + 1) % PLAYERS
