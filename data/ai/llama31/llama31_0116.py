import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates a new game board with specified dimensions"""
    board = []
    for _ in range(BOARD_ROWS):
        row = []
        for _ in range(BOARD_COLS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board):
    """Prints the game board with column labels"""
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        row_str = '|'
        for cell in row:
            row_str += ' ' + cell + ' |'
        print(row_str)
    print('+---+---+---+---+---+---+---+')

def get_player():
    """Randomly selects the first player"""
    return random.randint(0, PLAYERS - 1)

def get_player_checker(player):
    """Returns the checker symbol for the specified player"""
    return CHECKERS[player]

def get_column_index(col):
    """Converts column label to index"""
    return ord(col) - ord('A')

def is_valid_input(col):
    """Checks if the input is a valid column label"""
    if len(col)!= 1 or not col.isalpha():
        return False
    col_index = get_column_index(col)
    return 0 <= col_index < BOARD_COLS

def is_valid_move(board, col):
    """Checks if the move is valid (column not full)"""
    return board[0][get_column_index(col)] == ' '

def make_move(board, player, col):
    """Makes a move on the board"""
    for row in reversed(board):
        if row[get_column_index(col)] == ' ':
            row[get_column_index(col)] = get_player_checker(player)
            return

def check_win(board, player):
    """Checks if the player has won"""
    checker = get_player_checker(player)
    # Check horizontal
    for row in board:
        for i in range(BOARD_COLS - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == checker:
                return True
    # Check vertical
    for col in range(BOARD_COLS):
        for i in range(BOARD_ROWS - 3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == checker:
                return True
    return False

def check_draw(board):
    """Checks if the game is a draw"""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def game():
    board = create_board()
    player = get_player()
    while True:
        print_board(board)
        print(f"Player {get_player_checker(player)}, please enter a column:")
        col = input().upper()
        if not is_valid_input(col):
            print("Invalid input. Please enter a column label.")
            continue
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        make_move(board, player, col)
        if check_win(board, player):
            print_board(board)
            print(f"Player {get_player_checker(player)} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        player = (player + 1) % PLAYERS

if __name__ == "__main__":
    game()
