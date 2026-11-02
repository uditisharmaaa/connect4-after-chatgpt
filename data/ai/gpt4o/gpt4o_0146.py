import os
import random

# Constants for the game configuration
NUM_ROWS = 6
NUM_COLUMNS = 7
NUM_PLAYERS = 2
PLAYERS_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Adjust symbols based on the number of players

def print_board(board):
    """Function to print the current state of the board."""
    os.system('clear')  # Clear the console screen
    # Print column headers
    print("  " + "   ".join(chr(c) for c in range(ord('A'), ord('A') + NUM_COLUMNS)))
    print("+" + "---+" * NUM_COLUMNS)
    
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * NUM_COLUMNS)

def create_board():
    """Function to create a new game board initialized with empty spaces."""
    return [[" " for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def is_valid_column(col):
    """Function to check if the provided column input is valid."""
    return ord('A') <= ord(col) < ord('A') + NUM_COLUMNS

def is_column_full(board, col):
    """Function to check if the specified column is full."""
    return board[0][col] != " "

def play_turn(board, player):
    """Function for a player to play their turn."""
    while True:
        col_input = input(f"Player {PLAYERS_SYMBOLS[player]}, please enter a column: ").strip().upper()
        if len(col_input) == 1 and is_valid_column(col_input):
            col_index = ord(col_input) - ord('A')
            if not is_column_full(board, col_index):
                # Place the checker in the lowest available cell
                for row in reversed(board):
                    if row[col_index] == " ":
                        row[col_index] = PLAYERS_SYMBOLS[player]
                        return
            else:
                print("Column is full, turn is lost.")
                return
        else:
            print("Invalid input, please try again.")

def check_win(board, player_symbol):
    """Function to check if a player has won the game."""
    # Horizontal check
    for row in board:
        for c in range(NUM_COLUMNS - 3):
            if all(cell == player_symbol for cell in row[c:c+4]):
                return True

    # Vertical check
    for c in range(NUM_COLUMNS):
        for r in range(NUM_ROWS - 3):
            if all(board[r+i][c] == player_symbol for i in range(4)):
                return True

    # Diagonal check (\ direction)
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLUMNS - 3):
            if all(board[r+i][c+i] == player_symbol for i in range(4)):
                return True

    # Diagonal check (/ direction)
    for r in range(3, NUM_ROWS):
        for c in range(NUM_COLUMNS - 3):
            if all(board[r-i][c+i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    """Function to check if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def connect4():
    """Main function to run the Connect 4 game."""
    board = create_board()
    print_board(board)
    current_player = random.randint(0, NUM_PLAYERS - 1)  # Randomly select starting player

    while True:
        play_turn(board, current_player)
        print_board(board)

        if check_win(board, PLAYERS_SYMBOLS[current_player]):
            print(f"Player {PLAYERS_SYMBOLS[current_player]} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break
        
        # Alternate player turns
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    connect4()
