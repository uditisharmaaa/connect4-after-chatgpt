import random
import os

# Constants
ROWS = 6  # Number of rows
COLS = 7  # Number of columns
COLUMNS = 'ABCDEFG'  # Column labels
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Allowed player tokens (up to 5 players)
NUM_PLAYERS = 2  # Change between 2 and 5 to adjust the number of players

# Initialize the game board
def init_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Clear the console screen
def clear_screen():
    os.system('clear')

# Print the game board
def print_board(board):
    clear_screen()
    print("  " + " ".join(COLUMNS))  # Print column headers (A-G)
    for row in board:
        print("| " + " ".join(row) + " |")
    print("  " + "- " * COLS)

# Check if the column input is valid and not full
def valid_move(board, col):
    if col not in COLUMNS:
        return False
    col_index = COLUMNS.index(col)
    return board[0][col_index] == ' '

# Drop a player's token in the chosen column
def drop_piece(board, col, player):
    col_index = COLUMNS.index(col)
    for row in reversed(board):  # Start from the bottom row
        if row[col_index] == ' ':
            row[col_index] = player
            break

# Check for a win condition
def check_win(board, player):
    # Check horizontal, vertical, and diagonal matches
    for r in range(ROWS):
        for c in range(COLS):
            if c + 3 < COLS and all(board[r][c + i] == player for i in range(4)):
                return True
            if r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)):
                return True
            if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player for i in range(4)):
                return True
            if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == player for i in range(4)):
                return True
    return False

# Check for a draw condition (no empty spaces left)
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Game loop
def connect_4():
    # Initialize the board and randomly choose the first player
    board = init_board()
    players = PLAYERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    # Main game loop
    while True:
        print_board(board)
        print(f"Player {current_player}'s turn!")
        
        # Get and validate user input
        move = input(f"Choose a column ({' '.join(COLUMNS)}): ").strip().upper()
        while not valid_move(board, move):
            print("Invalid move. Please try again.")
            move = input(f"Choose a column ({' '.join(COLUMNS)}): ").strip().upper()

        # Make the move
        drop_piece(board, move, current_player)

        # Check for a win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = players.index(current_player)
        current_player = players[(current_player_index + 1) % NUM_PLAYERS]

# Run the game
if __name__ == "__main__":
    connect_4()
