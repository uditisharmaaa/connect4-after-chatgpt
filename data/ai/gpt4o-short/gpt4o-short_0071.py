import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Number of players
NUM_PLAYERS = 2  # You can change this to any value between 2 and 5

# Validate number of players
if not 2 <= NUM_PLAYERS <= 5:
    raise ValueError("Number of players must be between 2 and 5")

# Current player index
current_player_idx = random.randint(0, NUM_PLAYERS - 1)

def create_board():
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + " ".join(COLUMN_NAMES))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (NUM_COLS * 2 + 1))

def drop_piece(board, col, piece):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = piece
            return True
    return False

def is_valid_column(col):
    return 0 <= col < NUM_COLS

def is_column_not_full(board, col):
    return board[0][col] == ' '

def check_winner(board, piece):
    # Check horizontal locations
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row][col+i] == piece for i in range(4)):
                return True

    # Check vertical locations
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if all(board[row+i][col] == piece for i in range(4)):
                return True

    # Check for positively sloped diagonals
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row+i][col+i] == piece for i in range(4)):
                return True

    # Check for negatively sloped diagonals
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row-i][col+i] == piece for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(NUM_COLS))

def get_column_index(column_name):
    if column_name in COLUMN_NAMES:
        return COLUMN_NAMES.index(column_name)
    return -1

def play_game():
    board = create_board()
    game_over = False

    while not game_over:
        print_board(board)
        current_player_symbol = PLAYER_SYMBOLS[current_player_idx]

        # Input from player
        col_input = input(f"Player {current_player_idx+1} ({current_player_symbol}), choose a column (A-G): ").strip().upper()
        col = get_column_index(col_input)

        if is_valid_column(col) and is_column_not_full(board, col):
            drop_piece(board, col, current_player_symbol)

            if check_winner(board, current_player_symbol):
                game_over = True
                print_board(board)
                print(f"Player {current_player_idx+1} ({current_player_symbol}) wins!")

            elif is_draw(board):
                game_over = True
                print_board(board)
                print("It's a draw!")

            # Move to the next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        else:
            print("Invalid move. Please try again.")

# Start the game
play_game()
