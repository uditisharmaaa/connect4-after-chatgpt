import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """
    Create an empty board with the specified dimensions.
    """
    board = []
    for _ in range(BOARD_ROWS):
        row = [' ' for _ in range(BOARD_COLS)]
        board.append(row)
    return board

def print_board(board):
    """
    Print the current state of the board.
    """
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        row_str = '| '
        for cell in row:
            row_str += cell + ' | '
        print(row_str)
    print('+---+---+---+---+---+---+---+')

def is_valid_move(board, col):
    """
    Check if a move is valid (i.e., the column is not full).
    """
    return board[0][col] == ' '

def get_next_open_row(board, col):
    """
    Get the next open row in the specified column.
    """
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row

def drop_checker(board, col, checker):
    """
    Drop a checker into the specified column.
    """
    row = get_next_open_row(board, col)
    board[row][col] = checker

def winning_move(board, checker):
    """
    Check if the current player has won.
    """
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def is_draw(board):
    """
    Check if the game is a draw (i.e., the board is full).
    """
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def game():
    """
    Play the game.
    """
    os.system('clear')
    board = create_board()
    print_board(board)
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    players.remove(current_player)
    players.insert(0, current_player)

    while True:
        print(f"Player {current_player}, please enter a column (A-G):")
        move = input().upper()
        if move not in 'ABCDEFG':
            print("Invalid input. Please enter a letter between A and G.")
            continue
        col = ord(move) - ord('A')
        if not is_valid_move(board, col):
            print("Invalid move. Column is full.")
            continue
        drop_checker(board, col, current_player)
        os.system('clear')
        print_board(board)
        if winning_move(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        current_player = players[1]
        players.insert(0, players.pop())

game()
