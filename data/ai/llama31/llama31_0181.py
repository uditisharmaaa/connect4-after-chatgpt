import os
import random
import string

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized to whitespace."""
    return [[' ' for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLUMNS]))
    for row in board:
        print('+---' * BOARD_COLUMNS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLUMNS + '+')

def get_player_checker(player_id):
    """Get the checker symbol for the given player ID."""
    return CHECKERS[player_id % len(CHECKERS)]

def is_valid_move(board, column):
    """Check if the move is valid (i.e., the column is not full)."""
    return board[0][column] == ' '

def get_next_open_row(board, column):
    """Get the next open row in the given column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            return row

def drop_checker(board, column, player_id):
    """Drop the checker in the given column."""
    row = get_next_open_row(board, column)
    board[row][column] = get_player_checker(player_id)

def check_win(board, player_id):
    """Check if the given player has won."""
    checker = get_player_checker(player_id)
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True
    # Check vertical locations for win
    for col in range(BOARD_COLUMNS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw (i.e., the board is full)."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    # Initialize the board
    board = create_board()
    # Randomly select the first player
    num_players = 2
    player_id = random.randint(0, num_players - 1)
    # Game loop
    while True:
        # Print the current state of the board
        print_board(board)
        # Get the player's move
        while True:
            move = input(f"Player {get_player_checker(player_id)}, please enter a column (A-{string.ascii_uppercase[BOARD_COLUMNS - 1]}): ")
            if move.upper() in string.ascii_uppercase[:BOARD_COLUMNS]:
                column = ord(move.upper()) - ord('A')
                if is_valid_move(board, column):
                    break
                else:
                    print("Invalid move, column is full.")
            else:
                print("Invalid input, please try again.")
        # Drop the checker
        drop_checker(board, column, player_id)
        # Check for a win
        if check_win(board, player_id):
            print_board(board)
            print(f"Player {get_player_checker(player_id)} won!")
            break
        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        # Switch players
        player_id = (player_id + 1) % num_players

if __name__ == "__main__":
    main()
