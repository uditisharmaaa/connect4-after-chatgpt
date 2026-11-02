import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

# Functions
def create_board(rows, columns):
    """Create the game board with the specified dimensions."""
    return [[EMPTY_CELL for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the game board."""
    os.system('clear')
    column_labels = "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def get_valid_column(board, player):
    """Prompt player for a valid column."""
    while True:
        col_input = input(f"Player {player}, please enter a column: ").upper()
        if len(col_input) == 1 and 'A' <= col_input <= chr(65 + len(board[0]) - 1):
            column_index = ord(col_input) - 65
            if board[0][column_index] == EMPTY_CELL:  # Check if column is not full
                return column_index
            else:
                print("Column is full! Try a different column.")
        else:
            print("Invalid input! Enter a column letter.")

def place_checker(board, column, player_symbol):
    """Place the player's checker in the specified column."""
    for row in reversed(board):
        if row[column] == EMPTY_CELL:
            row[column] = player_symbol
            break

def check_win(board, player_symbol):
    """Check if the player has won the game."""
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for row in board:
        for col in range(cols - 3):
            if row[col] == row[col+1] == row[col+2] == row[col+3] == player_symbol:
                return True

    # Check vertical
    for col in range(cols):
        for row in range(rows - 3):
            if (board[row][col] == board[row+1][col] == 
                board[row+2][col] == board[row+3][col] == player_symbol):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if (board[row][col] == board[row+1][col+1] == 
                board[row+2][col+2] == board[row+3][col+3] == player_symbol):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if (board[row][col] == board[row-1][col+1] == 
                board[row-2][col+2] == board[row-3][col+3] == player_symbol):
                return True
                
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell != EMPTY_CELL for row in board for cell in row)

def main():
    # Initialize the board and settings
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Set to 2 players. Can be adjusted up to MAX_PLAYERS.
    players = PLAYER_SYMBOLS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    # Print the initial board
    print_board(board)

    # Game loop
    while True:
        # Current player's turn
        current_player = players[current_player_index]
        column = get_valid_column(board, current_player)
        place_checker(board, column, current_player)

        # Print updated board
        print_board(board)

        # Check for win or draw
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
