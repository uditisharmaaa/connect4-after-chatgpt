import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create an empty game board with the given dimensions."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """Print the current state of the game board."""
    # Print column labels
    print('  ' + ' '.join(string.ascii_uppercase[:cols]))
    print('+---' * cols + '+')
    
    # Print each row of the board
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * cols + '+')

def get_player_checker(player_num):
    """Return the checker for the given player number."""
    return CHECKERS[player_num - 1]

def get_next_player(player_num, num_players):
    """Return the number of the next player."""
    return (player_num % num_players) + 1

def is_valid_column(board, col, cols):
    """Check if the given column is valid and not full."""
    if col < 0 or col >= cols:
        return False
    return board[0][col] == ' '

def get_lowest_empty_space(board, col):
    """Return the row index of the lowest empty space in the given column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def place_checker(board, player_num, col):
    """Place the checker for the given player in the specified column."""
    checker = get_player_checker(player_num)
    row = get_lowest_empty_space(board, col)
    if row!= -1:
        board[row][col] = checker

def check_win(board, player_num):
    """Check if the given player has won the game."""
    checker = get_player_checker(player_num)
    
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col+1] == checker and board[row][col+2] == checker and board[row][col+3] == checker:
                return True
    
    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    
    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    
    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    
    return False

def check_draw(board):
    """Check if the game has ended in a draw."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                return False
    return True

def main():
    num_players = 2
    current_player = random.randint(1, num_players)
    board = create_board(BOARD_ROWS, BOARD_COLS)
    
    while True:
        os.system('clear')
        print_board(board, BOARD_COLS)
        print(f"Player {get_player_checker(current_player)}, please enter a column (A-{}):".format(string.ascii_uppercase[BOARD_COLS-1]))
        
        while True:
            try:
                col = string.ascii_uppercase.index(input().upper())
                if is_valid_column(board, col, BOARD_COLS):
                    break
                else:
                    print("Invalid column. Please try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
        
        place_checker(board, current_player, col)
        
        if check_win(board, current_player):
            os.system('clear')
            print_board(board, BOARD_COLS)
            print(f"Player {get_player_checker(current_player)} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board, BOARD_COLS)
            print("It's a draw!")
            break
        
        current_player = get_next_player(current_player, num_players)

if __name__ == "__main__":
    main()
