import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
BOARD_EMPTY_CELL = " "
COLUMN_LABELS = [chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Initialize global variables
board = [[BOARD_EMPTY_CELL] * COLUMNS for _ in range(ROWS)]
players_count = 2  # You can change this for more players (2-5 supported)
players_symbols = PLAYER_SYMBOLS[:players_count]
current_turn = random.choice(players_symbols)

def print_board():
    """Prints the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def validate_input(input_char):
    """Validates the user's input to ensure it is a capital letter within valid column range."""
    if input_char in COLUMN_LABELS:
        return COLUMN_LABELS.index(input_char)
    return None

def place_checker(column_index, player_symbol):
    """Places the player's checker in the lowest available space in the given column."""
    for row_index in reversed(range(ROWS)):
        if board[row_index][column_index] == BOARD_EMPTY_CELL:
            board[row_index][column_index] = player_symbol
            return True
    return False  # Column is full

def check_win():
    """Checks if there is a winning condition in the board for any player."""
    # Check horizontal, vertical, and diagonal lines for a win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] != BOARD_EMPTY_CELL:
                return board[row][col]

    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] != BOARD_EMPTY_CELL:
                return board[row][col]

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] != BOARD_EMPTY_CELL:
                return board[row][col]

            if board[row+3][col] == board[row+2][col+1] == board[row+1][col+2] == board[row][col+3] != BOARD_EMPTY_CELL:
                return board[row+3][col]

    return None

def check_draw():
    """Checks if the board is completely filled causing a draw."""
    return all(board[0][col] != BOARD_EMPTY_CELL for col in range(COLUMNS))

def play_game():
    """Main function to play the Connect 4 game."""
    global current_turn
    print_board()
    
    while True:
        player_input = input(f"Player {current_turn}, please enter a column: ")
        validated_column = validate_input(player_input)
        
        if validated_column is not None:
            if place_checker(validated_column, current_turn):
                print_board()
                winner = check_win()
                if winner:
                    print(f"Player {winner} won!")
                    break
                if check_draw():
                    print("The game is a draw!")
                    break
                current_turn = players_symbols[(players_symbols.index(current_turn) + 1) % players_count]
            else:
                print("Column is full, turn invalid!")
        else:
            print("Invalid input, please enter a valid column label.")

if __name__ == "__main__":
    play_game()
