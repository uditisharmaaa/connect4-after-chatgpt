import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Change the number of players here (2 to 5)

# Board setup
board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board():
    # Function to print the board
    os.system('clear')
    print(' '.join(COLUMN_LABELS))
    for row in board:
        print(' '.join(row))

def get_column_index(column_label):
    # Function to convert column label to index
    if column_label in COLUMN_LABELS:
        return COLUMN_LABELS.index(column_label)
    return -1

def is_valid_move(column_index):
    # Function to check if the move is valid (i.e., within bounds and not full)
    return 0 <= column_index < COLUMNS and board[0][column_index] == ' '

def make_move(player_symbol, column_index):
    # Function to place player's symbol in the desired column
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = player_symbol
            break

def check_winner(player_symbol):
    # Function to check if the current player has won
    # Horizontal check
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == player_symbol for i in range(4)):
                return True
    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True
    # Diagonal checks
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == player_symbol for i in range(4)):
                return True
    return False

def is_draw():
    # Function to check if the game is a draw (i.e., board is full)
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    # Main function to run the game
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    random.shuffle(players)
    
    # Randomly select the starting player
    current_player_index = 0
    print_board()

    while True:
        current_player = players[current_player_index]
        move = input(f"Player {current_player}'s turn, enter column (A-G): ").strip().upper()
        column_index = get_column_index(move)

        if not is_valid_move(column_index):
            print("Invalid move! Try again.")
            continue

        make_move(current_player, column_index)
        print_board()

        if check_winner(current_player):
            print(f"Player {current_player} wins!")
            break

        if is_draw():
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
