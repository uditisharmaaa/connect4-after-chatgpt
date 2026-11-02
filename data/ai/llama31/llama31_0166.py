import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D list filled with whitespaces."""
    return [[' ']*COLUMNS for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + ' '.join(chr(65+i) for i in range(COLUMNS)))
    print(' '+'-'*COLUMNS*3)
    for row in board:
        print('| '+' | '.join(row) + ' |')
        print(' '+'-'*COLUMNS*3)

def is_valid_move(board, column):
    """Check if a move is valid."""
    return column >= 0 and column < COLUMNS and board[0][column] == ' '

def get_next_open_row(board, column):
    """Get the next open row in a column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            return row

def drop_piece(board, row, column, piece):
    """Drop a piece into the board."""
    board[row][column] = piece

def winning_move(board, piece):
    """Check if a move is a winning move."""
    # Check horizontal locations for win
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def game_over(board):
    """Check if the game is over."""
    if winning_move(board, CHECKERS[0]):
        return True
    elif winning_move(board, CHECKERS[1]):
        return True
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    board = create_board()
    current_player = 0
    random.shuffle(CHECKERS)
    print("Player order: " + ', '.join(CHECKERS[:PLAYERS]))
    while True:
        print_board(board)
        column = input("Player " + CHECKERS[current_player] + ", choose a column: ")
        column = ord(column.upper()) - 65
        if is_valid_move(board, column):
            row = get_next_open_row(board, column)
            drop_piece(board, row, column, CHECKERS[current_player])
            if winning_move(board, CHECKERS[current_player]):
                print_board(board)
                print("Player " + CHECKERS[current_player] + " wins!")
                break
            if game_over(board):
                print_board(board)
                print("It's a draw!")
                break
            current_player = (current_player + 1) % PLAYERS
        else:
            print("Invalid move, try again.")

if __name__ == "__main__":
    main()
