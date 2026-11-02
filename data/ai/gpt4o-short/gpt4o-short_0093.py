import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change this between 2 and 5

def print_board(board):
    os.system('clear')
    print('  A B C D E F G')
    for row in board:
        print(' |'.join(row) + ' |')
    print()

def is_valid_move(board, col):
    return board[0][col] == ' '

def apply_move(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return

def check_win(board, player):
    # Check horizontal, vertical, and diagonal wins
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS - 3):
            if all(board[i][j + k] == player for k in range(4)):
                return True
    for i in range(NUM_ROWS - 3):
        for j in range(NUM_COLS):
            if all(board[i + k][j] == player for k in range(4)):
                return True
    for i in range(NUM_ROWS - 3):
        for j in range(NUM_COLS - 3):
            if all(board[i + k][j + k] == player for k in range(4)):
                return True
            if all(board[i + 3 - k][j + k] == player for k in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(NUM_COLS))

def get_player_input(current_player):
    while True:
        move = input(f"Player {current_player}, choose column A-G: ").upper()
        if move in 'ABCDEFG' and is_valid_move(board, ord(move) - ord('A')):
            return ord(move) - ord('A')
        print("Invalid move. Try again.")

def main():
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        col = get_player_input(PLAYERS[current_player_index])
        apply_move(board, col, PLAYERS[current_player_index])
        
        if check_win(board, PLAYERS[current_player_index]):
            print_board(board)
            print(f"Player {PLAYERS[current_player_index]} wins!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
