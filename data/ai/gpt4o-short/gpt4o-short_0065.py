import os
import random

# Constants
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # The set of possible players
NUM_PLAYERS = 2  # Modify this number to set between 2 to 5 players

# Board dimensions
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Create the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board with column labels
def print_board(board):
    os.system('clear')
    print(" ".join(COLUMN_LABELS))
    for row in board:
        print(" ".join(row))

# Validate the player's move
def is_valid_move(board, col):
    return col >= 0 and col < COLUMNS and board[0][col] == ' '

# Drop a piece into the board
def drop_piece(board, col, piece):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = piece
            return

# Check for a win
def check_win(board, piece):
    # Check horizontals, verticals and diagonals
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == piece for i in range(4)):
                return True
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == piece for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == piece for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == piece for i in range(4)):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Main game loop
def play_game():
    board = create_board()
    players = PLAYERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}'s turn.")
        move = input("Choose a column (A-G): ").strip().upper()

        if move in COLUMN_LABELS:
            column_index = COLUMN_LABELS.index(move)
            if is_valid_move(board, column_index):
                drop_piece(board, column_index, current_player)
                if check_win(board, current_player):
                    print_board(board)
                    print(f"Player {current_player} wins!")
                    break
                if check_draw(board):
                    print_board(board)
                    print("The game is a draw!")
                    break
                current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]
            else:
                print("Invalid move. Column is full.")
        else:
            print("Invalid input. Please choose a valid column.")

# Run the game
play_game()
