import os
import random

# Constants for the board dimensions and number of players
ROWS = 6
COLS = 7
MAX_PLAYERS = 5

# Characters representing the players
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clears the console screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates a game board with the specified dimensions."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board."""
    # Print column labels (A, B, C, ...)
    col_labels = '  '.join([chr(65 + i) for i in range(len(board[0]))])
    print(f"  {col_labels}")
    print('+---' * len(board[0]) + '+')

    # Print each row of the board
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * len(board[0]) + '+')

def is_valid_column(col, board):
    """Checks if a column is valid for placing a checker."""
    return 0 <= col < len(board[0]) and board[0][col] == ' '

def get_valid_column(player, board):
    """Prompts the player for a valid column and returns its index."""
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col_input) == 1 and 'A' <= col_input <= 'Z':
            col = ord(col_input) - ord('A')
            if is_valid_column(col, board):
                return col
        print("Invalid column. Please try again.")

def place_checker(col, player_marker, board):
    """Places the player's checker in the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player_marker
            break

def check_win(board, player_marker):
    """Checks if the player has won the game."""
    # Dimensions
    rows = len(board)
    cols = len(board[0])
    streak = 4  # Number needed to win

    # Check horizontal
    for r in range(rows):
        for c in range(cols - streak + 1):
            if all(board[r][c+i] == player_marker for i in range(streak)):
                return True

    # Check vertical
    for r in range(rows - streak + 1):
        for c in range(cols):
            if all(board[r+i][c] == player_marker for i in range(streak)):
                return True

    # Check diagonal (\)
    for r in range(rows - streak + 1):
        for c in range(cols - streak + 1):
            if all(board[r+i][c+i] == player_marker for i in range(streak)):
                return True

    # Check diagonal (/)
    for r in range(streak - 1, rows):
        for c in range(cols - streak + 1):
            if all(board[r-i][c+i] == player_marker for i in range(streak)):
                return True

    # No win found
    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to play the Connect 4 game."""
    # Initialize board and players
    board = create_board(ROWS, COLS)
    num_players = 2  # Fixed number of players for this assignment
    player_markers = PLAYER_MARKERS[:num_players]
    
    # Randomly choose the first player
    current_player_idx = random.randint(0, num_players - 1)

    # Game loop
    while True:
        clear_screen()
        print_board(board)

        # Get the current player's marker
        current_player = player_markers[current_player_idx]

        # Get a valid column from the player
        col = get_valid_column(current_player, board)

        # Place the checker
        place_checker(col, current_player, board)

        # Check for a win
        if check_win(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % num_players

# Start the game when this script is run
if __name__ == '__main__':
    play_game()
