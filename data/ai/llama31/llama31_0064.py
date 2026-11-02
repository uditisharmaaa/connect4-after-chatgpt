import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
PLAYERS_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D list filled with whitespaces."""
    return [[' ']*BOARD_COLS for _ in range(BOARD_ROWS)]

def print_board(board, players):
    """Print the current state of the board."""
    os.system('clear')
    print('  A B C D E F G')
    for row in board:
        print('+---+'*BOARD_COLS)
        print('|', end=' ')
        for cell in row:
            print(cell, end=' | ')
        print()
    print('+---+'*BOARD_COLS)
    print(f"Player {players[0]}, please enter a column: ")

def is_valid_input(input_str, players):
    """Check if the input is a valid column letter."""
    if len(input_str)!= 1:
        return False
    if not input_str.isalpha():
        return False
    if not 'A' <= input_str.upper() <= 'G':
        return False
    return True

def get_column_from_input(input_str):
    """Convert the input letter to a column index."""
    return ord(input_str.upper()) - ord('A')

def is_column_full(board, col):
    """Check if a column is already full."""
    return board[0][col]!= ' '

def drop_checker(board, col, checker):
    """Drop a checker into the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            break

def check_win(board, players):
    """Check if there's a winner."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col]!= ' ':
                # Check horizontal locations for win
                if col < BOARD_COLS - 3:
                    if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3]:
                        return board[row][col]
                # Check vertical locations for win
                if row < BOARD_ROWS - 3:
                    if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]:
                        return board[row][col]
                # Check positively sloped diagonals
                if row < BOARD_ROWS - 3 and col < BOARD_COLS - 3:
                    if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                        return board[row][col]
                # Check negatively sloped diagonals
                if row > 2 and col < BOARD_COLS - 3:
                    if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]:
                        return board[row][col]
    return None

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        if ' ' in row:
            return False
    return True

def game():
    players = PLAYERS_CHECKERS[:2]
    current_player = random.choice(players)
    board = create_board()
    while True:
        print_board(board, [current_player])
        input_str = input().upper()
        while not is_valid_input(input_str, players):
            input_str = input("Invalid input. Please enter a column letter (A-G): ").upper()
        col = get_column_from_input(input_str)
        if is_column_full(board, col):
            print("Column is full. Please choose another column.")
            continue
        drop_checker(board, col, current_player)
        winner = check_win(board, players)
        if winner:
            print_board(board, [current_player])
            print(f"Player {winner} won!")
            break
        if check_draw(board):
            print_board(board, [current_player])
            print("It's a draw!")
            break
        current_player = players[0] if current_player == players[1] else players[1]

game()
