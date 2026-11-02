import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # This can be changed from 2 to 5 depending on the game

# Initialize the game board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the screen (use 'cls' for Windows)
    print(' '.join(COLUMN_LABELS))
    for row in board:
        print(' '.join(row))
    print()

# Drop a piece into the board
def drop_piece(board, column, piece):
    for row in reversed(board):  # Start from the bottom row
        if row[column] == ' ':
            row[column] = piece
            return True
    return False

# Check for a winning move
def check_winner(board, piece):
    # Check horizontal, vertical, and diagonal for a winning set of four
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (c + 3 < COLUMNS and all(board[r][c+i] == piece for i in range(4))) or \
               (r + 3 < ROWS and all(board[r+i][c] == piece for i in range(4))) or \
               (r + 3 < ROWS and c + 3 < COLUMNS and all(board[r+i][c+i] == piece for i in range(4))) or \
               (r + 3 < ROWS and c - 3 >= 0 and all(board[r+i][c-i] == piece for i in range(4))):
                return True
    return False

# Check if the board is completely filled
def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Get column input from the player
def get_player_input(player):
    while True:
        choice = input(f"Player {player}, choose a column (A-G): ").upper()
        if choice in COLUMN_LABELS:
            return COLUMN_LABELS.index(choice)
        print("Invalid input. Please choose a column between A and G.")

# Main game function
def play_game():
    board = create_board()
    players = PLAYER_TOKENS[:NUM_PLAYERS]
    random.shuffle(players)  # Randomize player order
    current_player_index = 0

    while True:
        print_board(board)
        current_player = players[current_player_index]

        # Player chooses a column
        column = get_player_input(current_player)

        # Drop the piece and check for valid move
        if not drop_piece(board, column, current_player):
            print("Column is full. Choose another column.")
            continue

        # Check for a win
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Move to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
