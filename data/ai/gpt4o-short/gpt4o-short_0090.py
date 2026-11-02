import os
import random

# Constants and setup
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Player tokens
NUM_PLAYERS = 3  # Can be set from 2 to 5

def create_board():
    """Create a 6x7 empty board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the console
    print('  ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
    print()

def is_valid_move(board, column):
    """Check if a column is a valid move."""
    return board[0][column] == ' '

def make_move(board, column, player_symbol):
    """Place the player's symbol in the selected column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player_symbol
            break

def check_winner(board, player_symbol):
    """Check if the current player has won the game."""
    # Check horizontal, vertical, and diagonal (both directions) lines for a win
    for r in range(ROWS):
        for c in range(COLUMNS):
            if check_line(board, r, c, 0, 1, player_symbol) or \
               check_line(board, r, c, 1, 0, player_symbol) or \
               check_line(board, r, c, 1, 1, player_symbol) or \
               check_line(board, r, c, 1, -1, player_symbol):
                return True
    return False

def check_line(board, r, c, delta_r, delta_c, player_symbol):
    """Check a sequence of four spots for a win."""
    count = 0
    for i in range(4):
        if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_symbol:
            count += 1
            r += delta_r
            c += delta_c
        else:
            break
    return count == 4

def is_draw(board):
    """Check if the game is a draw (no empty spots left)."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    """Main game loop handling the Connect 4 game play."""
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)  # Random starting player

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}'s turn")

        column_choice = input("Choose a column (A-G): ").upper()
        while column_choice not in COLUMN_LABELS or not is_valid_move(board, COLUMN_LABELS.index(column_choice)):
            print("Invalid move. Try again.")
            column_choice = input("Choose a column (A-G): ").upper()

        make_move(board, COLUMN_LABELS.index(column_choice), current_player)
        
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        elif is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS  # Cycle through players

# To run the game
play_game()
