import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    os.system('clear')
    print('  A B C D E F G')
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

def is_valid_move(board, col):
    return board[0][col] == ' '

def get_next_open_row(board, col):
    for row in range(BOARD_ROWS-1, -1, -1):
        if board[row][col] == ' ':
            return row

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    num_players = 2
    players = [CHECKERS[i] for i in range(num_players)]
    current_player_index = random.randint(0, num_players-1)
    board = create_board()
    print_board(board)

    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column (A-G): ")
        col_choice = input().strip().upper()

        if not col_choice or not 'A' <= col_choice <= 'G':
            print("Invalid column choice. Please try again.")
            continue

        col_choice = ord(col_choice) - ord('A')

        if not is_valid_move(board, col_choice):
            print("Column is full. Please choose another column.")
            continue

        row = get_next_open_row(board, col_choice)
        drop_piece(board, row, col_choice, current_player)

        print_board(board)

        if winning_move(board, current_player):
            print(f"Player {current_player} wins!")
            break

        if draw_board(board):
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
