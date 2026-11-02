import os
import random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2  # Set number of players for the game

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('A B C D E F G')
    for row in board:
        print(' '.join(row))

def is_valid_move(board, col):
    return board[0][col] == ' '

def make_move(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            break

def check_win(board, player):
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLS):
            if col <= COLS - 4 and all(board[row][col + i] == player for i in range(4)):
                return True
            if row <= ROWS - 4 and all(board[row + i][col] == player for i in range(4)):
                return True
            if col <= COLS - 4 and row <= ROWS - 4 and all(board[row + i][col + i] == player for i in range(4)):
                return True
            if col >= 3 and row <= ROWS - 4 and all(board[row + i][col - i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def get_move():
    while True:
        move = input(f"Choose a column (A-G): ").strip().upper()
        if move in 'ABCDEFG':
            return ord(move) - ord('A')
        print("Invalid input. Please choose a column between A-G.")

def connect_4_game():
    board = create_board()
    players = PLAYERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}'s turn")
        col = get_move()
        
        if not is_valid_move(board, col):
            print("Column is full. Try again.")
            continue
        
        make_move(board, col, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    connect_4_game()
