import os
import random

# Constant global variables
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a 2D board with all elements initialized with whitespaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """Print the Connect 4 board."""
    print('  ' + '   '.join(chr(65 + i) for i in range(cols)))
    print('+---' + '+---' * (cols - 1))
    for row in board:
        print('|   ' + '|   '.join(row) + '|')
        print('+---' + '+---' * (cols - 1))

def is_valid_input(input_str, cols):
    """Check if the user input is valid."""
    return input_str.isalpha() and len(input_str) == 1 and 'A' <= input_str <= chr(65 + cols - 1)

def get_player_input(player, board, cols):
    """Get the player's input and validate it."""
    while True:
        input_str = input(f"Player {player}, please enter a column: ")
        if is_valid_input(input_str, cols):
            return ord(input_str) - 65
        else:
            print("Invalid input. Please try again.")

def place_checker(board, player, col):
    """Place the checker in the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return

def check_win(board, player, rows, cols):
    """Check if the player has won."""
    # Check horizontal wins
    for row in board:
        for i in range(cols - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == player:
                return True

    # Check vertical wins
    for col in range(cols):
        for i in range(rows - 3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] == player:
                return True

    # Check diagonal wins
    for row in range(rows - 3):
        for col in range(cols - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == player:
                return True
            if board[row][col + 3] == board[row + 1][col + 2] == board[row + 2][col + 1] == board[row + 3][col] == player:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    # Set the number of players
    num_players = 2

    # Create the board
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player = random.randint(0, num_players - 1)

    while True:
        os.system('clear')
        print_board(board, NUM_COLS)

        # Get the current player's input
        col = get_player_input(CHECKERS[current_player], board, NUM_COLS)

        # Place the checker
        place_checker(board, CHECKERS[current_player], col)

        # Check for a win
        if check_win(board, CHECKERS[current_player], NUM_ROWS, NUM_COLS):
            os.system('clear')
            print_board(board, NUM_COLS)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for a draw
        if check_draw(board):
            os.system('clear')
            print_board(board, NUM_COLS)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
