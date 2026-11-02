import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = "ABCDEFG"
EMPTY = '.'
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players can play

def create_board():
    """Creates the game board as a 2D list."""
    return [[EMPTY] * COLUMNS for _ in range(ROWS)]

def print_board(board):
    """Displays the current state of the game board."""
    os.system('clear')
    print(' '.join(COLUMN_LABELS))
    for row in board:
        print(' '.join(row))

def is_valid_input(input_str):
    """Checks if input is valid and returns corresponding column index."""
    return input_str in COLUMN_LABELS

def make_move(board, column, player):
    """Places the player's piece in the chosen column."""
    for row in reversed(board):
        if row[column] == EMPTY:
            row[column] = player
            return True
    return False

def check_win(board, player):
    """Check if the current player has won the game."""
    # Horizontal check
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == player for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Diagonal checks
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(EMPTY not in row for row in board)

def play_game():
    """Runs the complete game loop."""
    board = create_board()
    num_players = min(5, len(PLAYERS))  # Ensuring we do not exceed 5 players
    current_player_index = random.randint(0, num_players - 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}'s turn.")
        
        while True:
            column_input = input("Choose a column (A-G): ").upper()
            if is_valid_input(column_input):
                column_index = COLUMN_LABELS.index(column_input)
                if make_move(board, column_index, current_player):
                    break
                else:
                    print("Column is full. Choose another.")
            else:
                print("Invalid input. Choose a column (A-G).")

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    play_game()
