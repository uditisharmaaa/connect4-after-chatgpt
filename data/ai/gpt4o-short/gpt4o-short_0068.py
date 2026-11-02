import os
import random

# Constants
NUM_ROWS = 6
NUM_COLUMNS = 7
COLUMN_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Configure the number of players
NUM_PLAYERS = 2  # Can be set to 2, 3, 4, or 5

def initialize_board():
    return [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def display_board(board):
    os.system('clear')
    print(' '.join(COLUMN_NAMES))
    for row in board:
        print(' '.join(row))
    print()

def check_winner(board, player):
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row][col+i] == player for i in range(4)):
                return True
    
    # Check vertical
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if all(board[row+i][col] == player for i in range(4)):
                return True

    # Check diagonal (positive slope)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True

    # Check diagonal (negative slope)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(NUM_COLUMNS))

def make_move(board, player, column):
    for row in reversed(range(NUM_ROWS)):
        if board[row][column] == ' ':
            board[row][column] = player
            return True
    return False

def get_player_choice(players, current_player_index):
    while True:
        choice = input(f"Player {players[current_player_index]}'s turn. Choose a column (A-G): ").upper()
        if choice in COLUMN_NAMES:
            column_index = COLUMN_NAMES.index(choice)
            if board[0][column_index] == ' ':
                return column_index
            else:
                print("Column is full. Try again.")
        else:
            print("Invalid choice. Try again.")

def main():
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = initialize_board()
    random.shuffle(players)
    
    current_player_index = 0
    display_board(board)

    while True:
        column_index = get_player_choice(players, current_player_index)
        make_move(board, players[current_player_index], column_index)
        display_board(board)
        
        if check_winner(board, players[current_player_index]):
            print(f"Player {players[current_player_index]} wins!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
