import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:5]  # Set between 2 to 5 players as needed
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Creates an empty game board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the console (use 'cls' for Windows)
    print(' '.join(COLUMN_LABELS))
    for row in board:
        print(' '.join(row))
    print()

def get_column_index(column):
    """Converts column label (A-G) to column index."""
    if column in COLUMN_LABELS:
        return COLUMN_LABELS.index(column)
    return -1

def is_valid_move(board, col_index):
    """Checks if a column is a valid move."""
    return 0 <= col_index < COLUMNS and board[0][col_index] == ' '

def make_move(board, col_index, player):
    """Places a player's piece in the chosen column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = player
            break

def check_win(board, player):
    """Checks if the given player has won the game."""
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check vertical wins
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right) wins
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right) wins
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    """Main game loop."""
    board = create_board()
    total_players = len(PLAYERS)
    current_player_index = random.randint(0, total_players - 1)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}'s turn!")
        
        # Get and validate input
        move = input("Choose a column (A-G): ").strip().upper()
        col_index = get_column_index(move)
        if not is_valid_move(board, col_index):
            print("Invalid move. Try again.")
            input("Press Enter to continue...")
            continue
        
        # Make the move
        make_move(board, col_index, current_player)
        
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
        current_player_index = (current_player_index + 1) % total_players

if __name__ == "__main__":
    main()
