import os
import random
import string

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with the given dimensions."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---+---+---+---+---+---+---+')

def validate_input(input_str):
    """Validate the user's input."""
    if len(input_str)!= 1:
        return False
    if input_str not in string.ascii_uppercase:
        return False
    if input_str < 'A' or input_str > 'G':
        return False
    return True

def get_column(input_str):
    """Convert the user's input to a column index."""
    return ord(input_str) - ord('A')

def place_checker(board, player, column):
    """Place a checker in the given column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = CHECKERS[player]
            return

def check_win(board, player):
    """Check if the given player has won."""
    # Check horizontal wins
    for row in board:
        for i in range(NUM_COLS - 3):
            if row[i] == CHECKERS[player] and row[i+1] == CHECKERS[player] and row[i+2] == CHECKERS[player] and row[i+3] == CHECKERS[player]:
                return True
    # Check vertical wins
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if board[i][col] == CHECKERS[player] and board[i+1][col] == CHECKERS[player] and board[i+2][col] == CHECKERS[player] and board[i+3][col] == CHECKERS[player]:
                return True
    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == CHECKERS[player] and board[row+1][col+1] == CHECKERS[player] and board[row+2][col+2] == CHECKERS[player] and board[row+3][col+3] == CHECKERS[player]:
                return True
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == CHECKERS[player] and board[row-1][col+1] == CHECKERS[player] and board[row-2][col+2] == CHECKERS[player] and board[row-3][col+3] == CHECKERS[player]:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    # Create the board
    board = create_board()
    # Randomly select the first player
    player = random.randint(0, NUM_PLAYERS - 1)
    # Game loop
    while True:
        print_board(board)
        # Get the current player's input
        while True:
            input_str = input(f"Player {CHECKERS[player]}, please enter a column: ")
            if validate_input(input_str):
                column = get_column(input_str)
                if board[0][column]!= ' ':
                    print("Column is full, please choose another column.")
                else:
                    break
            else:
                print("Invalid input, please enter a letter between A and G.")
        # Place the checker
        place_checker(board, player, column)
        # Check for a win
        if check_win(board, player):
            print_board(board)
            print(f"Player {CHECKERS[player]} won!")
            break
        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        # Switch to the next player
        player = (player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
