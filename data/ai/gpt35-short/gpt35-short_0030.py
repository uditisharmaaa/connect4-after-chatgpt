import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change this from 2 to 5 as needed
PLAYERS = PLAYERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('=' * (COLS * 2 +1))

def get_player_move(player):
    while True:
        move = input(f"Player {player}, choose a column (A-G): ").upper()
        if move in COLUMN_LABELS:
            col = COLUMN_LABELS.index(move)
            return col
        else:
            print("Invalid input. Please enter a letter from A to G.")

def is_valid_move(board, col):
    return board[0][col] == ' '

def make_move(board, col, player):
    # Place piece in lowest empty spot in the column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_winner(board, player):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == player for i in range(4)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == player for i in range(4)):
                return True
    # Check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True
    # Check diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    # If top row has no space in any col, it's a draw
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board()
    players = PLAYERS
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Current player: {current_player}")

        col = get_player_move(current_player)
        if not is_valid_move(board, col):
            print("That column is full. Try again.")
            continue
        
        make_move(board, col, current_player)

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw! No more moves left.")
            break

        # Next player
        current_index = players.index(current_player)
        current_player = players[(current_index + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
