import os
import random

# Constant variables
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Create the board
def create_board():
    board = [[' ' for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
    return board

# Print the board
def print_board(board):
    os.system('clear')
    print('  A', end='')
    for col in range(BOARD_COLUMNS - 1):
        print('   ' + chr(ord('A') + col + 1), end='')
    print()
    print('+' + '---+' * BOARD_COLUMNS)
    for row in range(BOARD_ROWS):
        print('|', end='')
        for col in range(BOARD_COLUMNS):
            print(' ' + board[row][col] + ' |', end='')
        print()
        print('+' + '---+' * BOARD_COLUMNS)

# Get player input
def get_player_input(player):
    while True:
        col = input(f"Player {CHECKERS[player]}, please enter a column: ")
        if len(col)!= 1 or not col.isalpha() or ord(col) < ord('A') or ord(col) > ord('A') + BOARD_COLUMNS - 1:
            print("Invalid input. Please enter a letter from A to", chr(ord('A') + BOARD_COLUMNS - 1))
        else:
            return ord(col) - ord('A')

# Place checker
def place_checker(board, player, col):
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = CHECKERS[player]
            return

# Check for win
def check_win(board, player):
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == CHECKERS[player] and board[row][col + 1] == CHECKERS[player] and board[row][col + 2] == CHECKERS[player] and board[row][col + 3] == CHECKERS[player]:
                return True
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == CHECKERS[player] and board[row + 1][col] == CHECKERS[player] and board[row + 2][col] == CHECKERS[player] and board[row + 3][col] == CHECKERS[player]:
                return True
    # Check diagonal
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == CHECKERS[player] and board[row + 1][col + 1] == CHECKERS[player] and board[row + 2][col + 2] == CHECKERS[player] and board[row + 3][col + 3] == CHECKERS[player]:
                return True
            if board[row + 3][col] == CHECKERS[player] and board[row + 2][col + 1] == CHECKERS[player] and board[row + 1][col + 2] == CHECKERS[player] and board[row][col + 3] == CHECKERS[player]:
                return True
    return False

# Check for draw
def check_draw(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == ' ':
                return False
    return True

# Main game loop
def main():
    board = create_board()
    players = random.sample(range(NUM_PLAYERS), NUM_PLAYERS)
    current_player = 0
    while True:
        print_board(board)
        col = get_player_input(players[current_player])
        place_checker(board, players[current_player], col)
        if check_win(board, players[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[players[current_player]]} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
