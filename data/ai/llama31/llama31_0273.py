import os
import random

# Constant global variables
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
PLAYERS = 2

# Checkers for players
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """
    Creates a 2D board with all elements initialized with whitespaces.
    """
    board = [[' ' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    return board

def print_board(board):
    """
    Prints the current state of the board.
    """
    os.system('clear')
    print('  ' + '   '.join([chr(65 + i) for i in range(BOARD_WIDTH)]))
    for i in range(BOARD_HEIGHT):
        print('+---' * BOARD_WIDTH + '+')
        row = '|   ' * BOARD_WIDTH + '|'
        for j in range(BOARD_WIDTH):
            row = row.replace('|   ', '| ' + board[i][j] + ' ', 1)
        print(row)
    print('+---' * BOARD_WIDTH + '+')

def is_valid_input(input_str, board):
    """
    Checks if the input is a valid column letter.
    """
    return input_str.isalpha() and input_str.upper() in 'ABCDEFG' and board[0][ord(input_str.upper()) - 65] == ' '

def get_next_player(current_player):
    """
    Returns the next player in the sequence.
    """
    return (current_player + 1) % PLAYERS

def drop_checker(board, player, column):
    """
    Drops a checker in the specified column.
    """
    for i in range(BOARD_HEIGHT - 1, -1, -1):
        if board[i][column] == ' ':
            board[i][column] = CHECKERS[player]
            break

def check_win(board, player):
    """
    Checks if the current player has won.
    """
    # Check horizontal locations for win
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT):
            if board[r][c] == CHECKERS[player] and board[r][c+1] == CHECKERS[player] and board[r][c+2] == CHECKERS[player] and board[r][c+3] == CHECKERS[player]:
                return True

    # Check vertical locations for win
    for c in range(BOARD_WIDTH):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == CHECKERS[player] and board[r+1][c] == CHECKERS[player] and board[r+2][c] == CHECKERS[player] and board[r+3][c] == CHECKERS[player]:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == CHECKERS[player] and board[r+1][c+1] == CHECKERS[player] and board[r+2][c+2] == CHECKERS[player] and board[r+3][c+3] == CHECKERS[player]:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_WIDTH - 3):
        for r in range(3, BOARD_HEIGHT):
            if board[r][c] == CHECKERS[player] and board[r-1][c+1] == CHECKERS[player] and board[r-2][c+2] == CHECKERS[player] and board[r-3][c+3] == CHECKERS[player]:
                return True

def check_draw(board):
    """
    Checks if the game is a draw.
    """
    return all([all([cell!= ' ' for cell in row]) for row in board])

def main():
    board = initialize_board()
    players = list(range(PLAYERS))
    random.shuffle(players)
    current_player = players[0]
    while True:
        print_board(board)
        print('Player', CHECKERS[current_player], ', please enter a column:')
        input_str = input().upper()
        while not is_valid_input(input_str, board):
            print('Invalid input. Please enter a valid column letter:')
            input_str = input().upper()
        column = ord(input_str) - 65
        drop_checker(board, current_player, column)
        if check_win(board, current_player):
            print_board(board)
            print('Player', CHECKERS[current_player], 'won!')
            break
        elif check_draw(board):
            print_board(board)
            print('It\'s a draw!')
            break
        current_player = get_next_player(current_player)

if __name__ == '__main__':
    main()
