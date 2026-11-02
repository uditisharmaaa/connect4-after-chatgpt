import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = "ABCDEFG"
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Maximum 5 players

# Set the number of players to use
NUM_PLAYERS = 2  # You can change this from 2 to 5

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Use 'cls' on Windows
    print('  ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (COLUMNS * 2 + 1))

def is_valid_column(board, col):
    return 0 <= col < COLUMNS and board[0][col] == ' '

def make_move(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return

def check_winner(board, player):
    # Check horizontal, vertical, and diagonal (both directions)
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def get_player_input():
    while True:
        choice = input("Choose a column (A-G): ").strip().upper()
        if choice in COLUMN_LABELS:
            return COLUMN_LABELS.index(choice)
        print("Invalid input, please choose a valid column (A-G).")

def main():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print(f"Player {PLAYERS[current_player_index]} will start!")

    while True:
        print_board(board)

        # Get user input
        col = get_player_input()

        # Validate the move
        if not is_valid_column(board, col):
            print("Column is full or invalid, please choose another one.")
            continue

        # Make the move
        make_move(board, col, PLAYERS[current_player_index])

        # Check for a win
        if check_winner(board, PLAYERS[current_player_index]):
            print_board(board)
            print(f"Player {PLAYERS[current_player_index]} wins!")
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
