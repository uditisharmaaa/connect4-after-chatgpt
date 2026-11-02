import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized with whitespaces."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + ' '.join(chr(65 + i) for i in range(NUM_COLS)))
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * NUM_COLS + '+')

def get_player_checker(player_id):
    """Get the checker symbol for the given player ID."""
    return CHECKERS[player_id]

def is_valid_input(input_str):
    """Check if the input is a valid column letter."""
    return input_str.isalpha() and len(input_str) == 1 and 'A' <= input_str <= 'G'

def get_player_move(player_id):
    """Get the player's move and validate the input."""
    while True:
        move = input(f"Player {get_player_checker(player_id)}, please enter a column: ").strip().upper()
        if is_valid_input(move):
            return ord(move) - 65

def place_checker(board, player_id, col):
    """Place the checker at the lowest available space in the column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = get_player_checker(player_id)
            return

def check_win(board, player_id):
    """Check if the given player has won."""
    checker = get_player_checker(player_id)

    # Check horizontal locations for win
    for row in board:
        for col in range(NUM_COLS - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    board = create_board()
    print_board(board)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        col = get_player_move(current_player)
        place_checker(board, current_player, col)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {get_player_checker(current_player)} won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
