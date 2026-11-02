import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with the given dimensions."""
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board, player_turn):
    """Print the current state of the board."""
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| {} | {} | {} | {} | {} | {} | {} |'.format(*row))
    print('+---+---+---+---+---+---+---+')
    print('Player {}, please enter a column:'.format(CHECKERS[player_turn]))

def is_valid_input(input_str):
    """Check if the user input is a valid column letter."""
    return input_str.upper() >= 'A' and input_str.upper() <= chr(ord('A') + NUM_COLS - 1)

def get_column_from_input(input_str):
    """Convert the user input to a column index."""
    return ord(input_str.upper()) - ord('A')

def is_valid_move(board, column):
    """Check if the move is valid (i.e., the column is not full)."""
    return board[0][column] == ' '

def make_move(board, player, column):
    """Make a move on the board."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = CHECKERS[player]
            break

def check_win(board, player):
    """Check if the player has won."""
    # Check horizontal wins
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == CHECKERS[player] and \
               board[row][col + 1] == CHECKERS[player] and \
               board[row][col + 2] == CHECKERS[player] and \
               board[row][col + 3] == CHECKERS[player]:
                return True

    # Check vertical wins
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if board[row][col] == CHECKERS[player] and \
               board[row + 1][col] == CHECKERS[player] and \
               board[row + 2][col] == CHECKERS[player] and \
               board[row + 3][col] == CHECKERS[player]:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == CHECKERS[player] and \
               board[row + 1][col + 1] == CHECKERS[player] and \
               board[row + 2][col + 2] == CHECKERS[player] and \
               board[row + 3][col + 3] == CHECKERS[player]:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == CHECKERS[player] and \
               board[row - 1][col + 1] == CHECKERS[player] and \
               board[row - 2][col + 2] == CHECKERS[player] and \
               board[row - 3][col + 3] == CHECKERS[player]:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == ' ':
                return False
    return True

def main():
    board = create_board()
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player = 0

    while True:
        print_board(board, current_player)
        input_str = input().strip()
        if not is_valid_input(input_str):
            print("Invalid input. Please enter a column letter.")
            continue
        column = get_column_from_input(input_str)
        if not is_valid_move(board, column):
            print("Column is full. Please choose another column.")
            continue
        make_move(board, current_player, column)
        if check_win(board, current_player):
            print_board(board, current_player)
            print("Player {} won!".format(CHECKERS[current_player]))
            break
        if check_draw(board):
            print_board(board, current_player)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
