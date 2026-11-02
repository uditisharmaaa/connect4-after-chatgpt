import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Symbols for the players

def create_board(rows, columns):
    """Create a game board with the given dimensions, initialized with white spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the game board with column labels."""
    os.system('clear')  # Clear the terminal screen
    headers = '  ' + '   '.join(chr(i + 65) for i in range(len(board[0])))
    print(headers)
    for row in board:
        print('+---' * len(row) + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * len(board[0]) + '+')

def is_valid_input(input_value, columns):
    """Check if the user input is a valid column letter."""
    return len(input_value) == 1 and input_value.isalpha() and ord(input_value.upper()) - 65 < columns

def get_lowest_empty_row(board, col_index):
    """Get the lowest empty row index for a given column, -1 if full."""
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][col_index] == ' ':
            return row_index
    return -1

def check_winner(board, player):
    """Check the board for any winning configurations for the given player."""
    # Horizontal check
    for row in board:
        for col in range(len(row) - 3):
            if all(cell == player for cell in row[col:col + 4]):
                return True
    
    # Vertical check
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[r][col] == player for r in range(row, row + 4)):
                return True

    # Diagonal checks (bottom left to top right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Diagonal checks (top left to bottom right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full and no player has won."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to play the Connect 4 game."""
    board = create_board(ROWS, COLUMNS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    players = PLAYERS[:NUM_PLAYERS]
    print_board(board)

    while True:
        current_player = players[current_player_idx]
        column_input = input(f"Player {current_player}, please enter a column: ").upper()
        
        if not is_valid_input(column_input, COLUMNS):
            print("Invalid input. Try again.")
            continue

        col_index = ord(column_input) - 65  # Convert column letter to index
        row_index = get_lowest_empty_row(board, col_index)

        if row_index == -1:
            print("Column is full. Turn lost.")
        else:
            board[row_index][col_index] = current_player

            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break

            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

            # Alternate players
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        
        print_board(board)

play_game()
