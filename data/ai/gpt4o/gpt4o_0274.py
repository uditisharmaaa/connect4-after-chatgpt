import os
import random

# Constants
NUM_ROWS = 6
NUM_COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_TO_WIN = 4

def create_board():
    """Create a board with dimensions NUM_ROWS x NUM_COLUMNS initialized with spaces."""
    return [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the game board."""
    os.system('clear')  # to clear the terminal screen
    column_labels = ' '.join(chr(c) for c in range(ord('A'), ord('A') + NUM_COLUMNS))
    print(f"  {column_labels} ")
    for row in board:
        print('+---' * NUM_COLUMNS + '+')
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
    print('+---' * NUM_COLUMNS + '+')

def is_valid_column(column):
    """Check if the column exists on the board."""
    return 'A' <= column < chr(ord('A') + NUM_COLUMNS)

def get_available_row(board, column):
    """Find the first available row in the column."""
    for row_idx in range(NUM_ROWS-1, -1, -1):
        if board[row_idx][column] == ' ':
            return row_idx
    return None

def check_win(board, player):
    """Check if the current player has a winning condition."""
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS - NUM_TO_WIN + 1):
            if all(board[row][col + offset] == player for offset in range(NUM_TO_WIN)):
                return True

    # Check vertical
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - NUM_TO_WIN + 1):
            if all(board[row + offset][col] == player for offset in range(NUM_TO_WIN)):
                return True

    # Check diagonal (positive slope)
    for row in range(NUM_ROWS - NUM_TO_WIN + 1):
        for col in range(NUM_COLUMNS - NUM_TO_WIN + 1):
            if all(board[row + offset][col + offset] == player for offset in range(NUM_TO_WIN)):
                return True

    # Check diagonal (negative slope)
    for row in range(NUM_TO_WIN - 1, NUM_ROWS):
        for col in range(NUM_COLUMNS - NUM_TO_WIN + 1):
            if all(board[row - offset][col + offset] == player for offset in range(NUM_TO_WIN)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game loop."""
    board = create_board()
    num_players = 2  # Set number of players, for assignment submission
    current_player_idx = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        current_player = PLAYERS[current_player_idx]
        print(f"Player {current_player}, please enter a column:")
        
        while True:
            column_input = input().strip().upper()
            if is_valid_column(column_input):
                column_index = ord(column_input) - ord('A')
                row_index = get_available_row(board, column_index)
                
                if row_index is not None:
                    board[row_index][column_index] = current_player
                    break
                else:
                    print(f"Column {column_input} is full!")
            else:
                print(f"Invalid column {column_input}. Please enter a valid column:")
        
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print("The game is a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
