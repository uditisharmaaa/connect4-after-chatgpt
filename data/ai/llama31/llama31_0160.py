import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Function to create the board
def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    print('  ' + ' '.join(chr(65+i) for i in range(COLUMNS)))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLUMNS + '+')

# Function to validate user input
def validate_input(column):
    if not column.isalpha():
        return False
    if not 'A' <= column.upper() <= chr(64 + COLUMNS):
        return False
    return True

# Function to place a checker
def place_checker(board, player, column):
    column = ord(column.upper()) - 65
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return True
    return False

# Function to check for a win
def check_win(board, player):
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == player and row[i+1] == player and row[i+2] == player and row[i+3] == player:
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == player and board[i+1][col] == player and board[i+2][col] == player and board[i+3][col] == player:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True
    return False

# Function to check for a draw
def check_draw(board):
    return all(cell!= ' ' for row in board for cell in row)

# Main function
def main():
    # Create the board
    board = create_board(ROWS, COLUMNS)

    # Randomly select the first player
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        # Clear the screen
        os.system('clear')

        # Print the board
        print_board(board)

        # Get the current player's name
        player_name = 'Player ' + CHECKERS[current_player]

        # Ask the current player for input
        while True:
            column = input(player_name + ', please enter a column: ').upper()
            if validate_input(column):
                break
            print('Invalid input. Please try again.')

        # Place the checker
        if not place_checker(board, CHECKERS[current_player], column):
            print('Column is full. Please try again.')
            continue

        # Check for a win
        if check_win(board, CHECKERS[current_player]):
            print_board(board)
            print(player_name + ' won!')
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print('It\'s a draw!')
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == '__main__':
    main()
