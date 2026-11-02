import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Can be adjusted to 2 to 5
COLUMN_LABELS = 'ABCDEFG'

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Display the board
def print_board(board):
    os.system('clear')
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')

# Check if a column is valid and not full
def is_valid_move(board, column):
    return 0 <= column < COLS and board[0][column] == ' '

# Drop a disc in the board
def drop_disc(board, column, player):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            break

# Check for a win condition
def check_win(board, player):
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLS):
            # Horizontal
            if col + 3 < COLS and all(board[row][col + i] == player for i in range(4)):
                return True
            # Vertical
            if row + 3 < ROWS and all(board[row + i][col] == player for i in range(4)):
                return True
            # Diagonal /
            if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == player for i in range(4)):
                return True
            # Diagonal \
            if row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == player for i in range(4)):
                return True
    return False

# Check for a draw condition
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

# Play the game
def play_game():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}'s turn")
        
        while True:
            try:
                column_input = input(f"Choose a column ({COLUMN_LABELS}): ").upper()
                if column_input in COLUMN_LABELS:
                    column = COLUMN_LABELS.index(column_input)
                    if is_valid_move(board, column):
                        break
                print("Invalid move. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Try again.")

        drop_disc(board, column, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Configure number of players and start the game
NUM_PLAYERS = 2  # Change this to number of players you want (2 to 5)
play_game()
