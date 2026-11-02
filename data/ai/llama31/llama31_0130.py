import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    # Create an empty board with whitespace characters
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    # Print the board with column labels and row separators
    print('  A B C D E F G')
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

def get_player_checker(player_index):
    # Get the checker for the current player
    return CHECKERS[player_index % len(CHECKERS)]

def is_valid_move(board, col):
    # Check if the column is not full
    return board[0][col] == ' '

def get_next_open_row(board, col):
    # Find the next open row in the column
    for row in range(BOARD_ROWS-1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def make_move(board, player_index, col):
    # Make a move by placing the checker in the next open row
    row = get_next_open_row(board, col)
    if row!= -1:
        board[row][col] = get_player_checker(player_index)
        return True
    return False

def check_win(board, player_index):
    # Check for a win by looking for 4 consecutive checkers
    checker = get_player_checker(player_index)
    # Check horizontal locations for win
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # Check positively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # Check negatively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def check_draw(board):
    # Check if the board is full
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def game():
    # Initialize the game
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)  # Randomly select the first player
    current_player_index = 0

    while True:
        # Clear the screen and print the board
        os.system('clear')
        print_board(board)
        # Get the current player's move
        col = input(f"Player {get_player_checker(current_player_index)}, please enter a column (A-G): ")
        col = ord(col.upper()) - ord('A')
        if not is_valid_move(board, col):
            print("Invalid move, try again.")
            continue
        # Make the move
        if not make_move(board, current_player_index, col):
            print("Invalid move, try again.")
            continue
        # Check for a win or draw
        if check_win(board, current_player_index):
            os.system('clear')
            print_board(board)
            print(f"Player {get_player_checker(current_player_index)} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    game()
