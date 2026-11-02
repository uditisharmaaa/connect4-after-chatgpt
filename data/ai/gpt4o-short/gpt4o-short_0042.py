import os
import random

# Constants for configuration
NUM_ROWS = 6
NUM_COLS = 7
COLUMNS = 'ABCDEFG'
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Select number of players (2 to 5)
NUM_PLAYERS = 3  # Adjust this as needed

def create_board():
    """Create an empty Connect 4 board."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def print_board(board):
    """Print the current state of the Connect 4 board."""
    clear_screen()
    print('  '.join(COLUMNS))
    for row in board:
        print(' | '.join(row))
        print('-' * (NUM_COLS * 4 - 1))

def get_column_index(column_letter):
    """Convert column letter to index."""
    if column_letter in COLUMNS:
        return COLUMNS.index(column_letter)
    return -1

def is_valid_move(board, column):
    """Check if a move is valid (i.e., column is not full)."""
    return board[0][column] == ' '

def make_move(board, column, player):
    """Place the player's piece in the chosen column."""
    for row in range(NUM_ROWS-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player
            return

def has_won(board, player):
    """Check for a win condition."""
    # Check horizontal, vertical, and diagonal (both directions) for 4 in a row
    # Horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Vertical
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Diagonal down-right
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Diagonal up-right
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    """Determine if the game is a draw (i.e., the board is full without a winner)."""
    return all(board[0][col] != ' ' for col in range(NUM_COLS))

def play_game():
    """Main game function to control the flow of the Connect 4 game."""
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        print_board(board)
        current_player = PLAYERS[current_player_index]

        # Get and validate player's move
        while True:
            move = input(f"Player {current_player}'s turn. Select column (A-G): ").strip().upper()
            column = get_column_index(move)
            if column != -1 and is_valid_move(board, column):
                make_move(board, column, current_player)
                break
            else:
                print("Invalid move. Try again.")

        # Check for a win or a draw
        if has_won(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            game_over = True
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Move to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
