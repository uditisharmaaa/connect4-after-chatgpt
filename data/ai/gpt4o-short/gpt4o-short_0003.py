import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
EMPTY_SLOT = '.'


def clear_screen():
    """Clear the console screen."""
    os.system('clear')


def create_board():
    """Create an empty game board."""
    return [[EMPTY_SLOT for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the game board."""
    clear_screen()
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print(' '.join(row))


def get_player_input(current_player):
    """Get and validate player input for the column choice."""
    while True:
        choice = input(f"Player {current_player}, select a column (A-G): ").upper()
        if choice in COLUMN_LABELS:
            return COLUMN_LABELS.index(choice)
        print("Invalid input. Please select a valid column (A-G).")


def place_disc(board, column, player_symbol):
    """Place a disc in the chosen column, if possible."""
    for row in reversed(board):
        if row[column] == EMPTY_SLOT:
            row[column] = player_symbol
            return True
    return False


def check_win(board, player_symbol):
    """Check for a winning condition: horizontal, vertical, or diagonal."""
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == player_symbol:
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == player_symbol:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == player_symbol:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == player_symbol:
                return True

    return False


def check_draw(board):
    """Check if the game is a draw."""
    return all(slot != EMPTY_SLOT for row in board for slot in row)


def play_game(num_players):
    """Main game loop for Connect 4."""
    board = create_board()
    players = PLAYER_SYMBOLS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    while True:
        current_player = players[current_player_index]
        print_board(board)

        column = get_player_input(current_player)

        if place_disc(board, column, current_player):
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                break
            elif check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            # Switch to the next player
            current_player_index = (current_player_index + 1) % num_players
        else:
            print("Column is full. Please choose a different column.")


# Set number of players (between 2 and 5)
NUM_PLAYERS = 3  # Can be adjusted between 2 and 5

if __name__ == "__main__":
    play_game(NUM_PLAYERS)
