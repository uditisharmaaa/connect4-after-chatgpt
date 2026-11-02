import os
import random

# Constant global variables
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a 2D board with the specified rows and columns"""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board"""
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+' * BOARD_COLS)
        print('|', end=' ')
        for cell in row:
            print(f' {cell} |', end=' ')
        print()
    print('+---+' * BOARD_COLS)

def is_valid_move(board, col):
    """Check if a move is valid (column is not full)"""
    return board[0][col] == ' '

def get_next_open_row(board, col):
    """Get the next open row in a column"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row

def drop_checker(board, row, col, checker):
    """Drop a checker into a column"""
    board[row][col] = checker

def winning_move(board, checker):
    """Check if a player has won"""
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

def draw_board(board):
    """Check if the board is full (draw)"""
    for col in range(BOARD_COLS):
        if is_valid_move(board, col):
            return False
    return True

def main():
    num_players = 2
    players = CHECKERS[:num_players]
    current_player = random.choice(players)

    board = create_board(BOARD_ROWS, BOARD_COLS)
    print_board(board)

    while True:
        os.system('clear')
        print_board(board)
        print(f'Player {current_player}, please enter a column (A-{chr(64 + BOARD_COLS)}):')

        move = input().upper()
        col = ord(move) - 65

        if not 0 <= col < BOARD_COLS:
            print('Invalid column. Please try again.')
            continue

        if not is_valid_move(board, col):
            print('Column is full. Please try again.')
            continue

        row = get_next_open_row(board, col)
        drop_checker(board, row, col, current_player)

        if winning_move(board, current_player):
            os.system('clear')
            print_board(board)
            print(f'Player {current_player} won!')
            break
        elif draw_board(board):
            os.system('clear')
            print_board(board)
            print('It\'s a draw!')
            break

        current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == '__main__':
    main()
