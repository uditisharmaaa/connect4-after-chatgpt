import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Can be up to 5 players

# Configuration: Set number of players (2 to 5)
NUM_PLAYERS = 3  # Change this to 2, 3, 4, or 5

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print(' '.join(COLUMN_LABELS))
    for row in board:
        print(' '.join(row))
    print()

def check_win(board, player):
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == player for i in range(4)):
                return True
    # Check vertical wins
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == player for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right) wins
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right) wins
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def drop_disc(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def get_move(player):
    while True:
        move = input(f"Player {player}, enter your move (A-G): ").strip().upper()
        if move in COLUMN_LABELS:
            col = COLUMN_LABELS.index(move)
            return col
        else:
            print("Invalid input. Please enter a letter between A and G.")

def main():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    players = PLAYERS[:NUM_PLAYERS]

    while True:
        print_board(board)
        current_player = players[current_player_index]
        col = get_move(current_player)
        
        if not drop_disc(board, col, current_player):
            print("Column is full. Try again.")
            continue
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
