import random
import os

# Constants for the game setup
NUM_ROWS = 6
NUM_COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2

CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]

def create_board(rows, columns):
    """Create an empty game board."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the game board."""
    os.system('clear')  # Clear the game screen
    column_labels = ' '.join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * len(board[0]) + '+')

def is_valid_column(column, board):
    """Check if a column choice is valid."""
    if column.isalpha() and len(column) == 1:
        index = ord(column.upper()) - 65
        if 0 <= index < len(board[0]) and board[0][index] == ' ':
            return True
    return False

def place_checker(column, board, checker):
    """Place a checker in the chosen column."""
    index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[index] == ' ':
            row[index] = checker
            break

def check_winner(board, checker):
    """Check for a win condition: 4 checkers in a row."""
    rows, columns = len(board), len(board[0])

    # Horizontal check
    for row in board:
        for col in range(columns - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(columns):
        for row in range(rows - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal checks
    for row in range(rows - 3):
        for col in range(columns - 3):
            # Diagonal from top-left to bottom-right
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
            # Diagonal from bottom-left to top-right
            if all(board[row + 3 - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to play Connect 4."""
    board = create_board(NUM_ROWS, NUM_COLUMNS)
    current_player = random.choice(PLAYER_SYMBOLS)
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        column = input().strip().upper()

        if is_valid_column(column, board):
            place_checker(column, board, current_player)
            print_board(board)

            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break

            if check_draw(board):
                print("The game is a draw!")
                break

            # Alternate turn to next player
            current_player = PLAYER_SYMBOLS[(PLAYER_SYMBOLS.index(current_player) + 1) % NUM_PLAYERS]
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    play_game()
