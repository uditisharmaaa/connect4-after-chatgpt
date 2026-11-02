import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a 2D board with whitespaces"""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board with column labels"""
    print('  A B C D E F G')
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

def get_player_checker(player_id):
    """Get the checker symbol for a player"""
    return CHECKERS[player_id % len(CHECKERS)]

def is_valid_input(col):
    """Check if the input column is valid"""
    return col in 'ABCDEFG' and col < chr(BOARD_COLS + 65)

def get_next_available_row(board, col):
    """Get the next available row in a column"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][ord(col) - 65] == ' ':
            return row
    return -1

def place_checker(board, col, checker):
    """Place a checker in a column"""
    row = get_next_available_row(board, col)
    if row!= -1:
        board[row][ord(col) - 65] = checker
        return True
    return False

def check_win(board, checker):
    """Check for a win in the board"""
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

def check_draw(board):
    """Check for a draw in the board"""
    return all([all([cell!= ' ' for cell in row]) for row in board])

def main():
    num_players = 2  # Set to 2 players for submission
    board = create_board(BOARD_ROWS, BOARD_COLS)
    current_player = random.randint(0, num_players - 1)

    while True:
        os.system('clear')
        print_board(board)
        checker = get_player_checker(current_player)
        print(f"Player {checker}, please enter a column: ")

        while True:
            col = input().upper()
            if is_valid_input(col):
                if place_checker(board, col, checker):
                    break
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input, please enter a column letter.")

        if check_win(board, checker):
            os.system('clear')
            print_board(board)
            print(f"Player {checker} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
