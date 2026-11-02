import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with dimensions BOARD_ROWS x BOARD_COLS"""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    print('+---' * BOARD_COLS + '+')
    for row in board:
        print('|   ' * BOARD_COLS + '|')
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_COLS + '+')

def validate_input(column):
    """Validate user input for column selection"""
    if not column.isalpha():
        return False
    if not column.upper() in string.ascii_uppercase[:BOARD_COLS]:
        return False
    return True

def place_checker(board, column, player):
    """Place a checker in the specified column for the given player"""
    column = string.ascii_uppercase.index(column.upper())
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player
            return

def check_win(board, player):
    """Check for a win condition in all directions"""
    # Horizontal check
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Vertical check
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Diagonal check (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Diagonal check (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw (board is full)"""
    return all([cell!= ' ' for row in board for cell in row])

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {current_player}, please enter a column: ")
        column = input().strip()

        if not validate_input(column):
            print("Invalid input. Please try again.")
            continue

        place_checker(board, column, current_player)

        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
