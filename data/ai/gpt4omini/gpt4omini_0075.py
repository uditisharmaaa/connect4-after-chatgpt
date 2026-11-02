import os
import random

# Constants for the game dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Players' markers
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Create an empty board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the console
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    print('+---' + ('+---' * (COLS - 1)) + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' + ('+---' * (COLS - 1)) + '+')

# Check for valid input from the player
def get_valid_input(current_player):
    while True:
        col_input = input(f'Player {PLAYERS[current_player]}, please enter a column (A-{chr(65 + COLS - 1)}): ').upper()
        if len(col_input) == 1 and 'A' <= col_input <= chr(65 + COLS - 1):
            col = ord(col_input) - 65
            if board[0][col] == ' ':
                return col
            else:
                print("That column is full. Please choose another.")
        else:
            print("Invalid input. Please enter a valid column letter.")

# Place the checker in the board
def place_checker(board, col, current_player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = PLAYERS[current_player]
            return True
    return False

# Check for a win
def check_winner(board):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] != ' ':
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] != ' ':
                return True

    # Check diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] != ' ':
                return True

    # Check diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] != ' ':
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game function
def main():
    global board
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        col = get_valid_input(current_player)

        # Place the checker
        place_checker(board, col, current_player)

        # Check for a win
        if check_winner(board):
            print_board(board)
            print(f'Player {PLAYERS[current_player]} won!')
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch players
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
