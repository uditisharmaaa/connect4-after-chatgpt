import random
import os

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Modify the number of players here (between 2 and 5)
NUM_PLAYERS = 2

# Ensure only valid number of players are set
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5"

# Initialize the board
def init_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clears the screen
    print(" A  B  C  D  E  F  G")
    for row in board:
        print('|' + '|'.join(row) + '|')
    print("-" * (COLUMNS * 3))

# Check for a win
def check_win(board, symbol):
    # Check horizontal locations for win
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == symbol for i in range(4)):
                return True

    # Check vertical locations for win
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == symbol for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == symbol for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == symbol for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

# Place a piece in the board
def place_piece(board, column, symbol):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = symbol
            return True
    return False  # Column is full

# Map input character to board column index
def col_to_index(col):
    return ord(col.upper()) - ord('A')

# Main game function
def play_game():
    board = init_board()
    game_over = False
    turn = random.randint(0, NUM_PLAYERS - 1)  # Randomly select first player

    while not game_over:
        print_board(board)
        current_symbol = PLAYER_SYMBOLS[turn]

        # Get and validate user input
        valid_input = False
        while not valid_input:
            move = input(f"Player {current_symbol}, choose a column (A-G): ").strip()
            if len(move) == 1 and 'A' <= move.upper() <= 'G':
                col = col_to_index(move)
                if board[0][col] == ' ':  # Check if the top of the column is empty
                    valid_input = True

        # Place the piece
        place_piece(board, col, current_symbol)

        # Check for win
        if check_win(board, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} wins!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True

        # Switch turn
        turn = (turn + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
