import os
import random

# Constants for the board dimensions and number of players
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear')
    header = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(header)
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_input(input_str):
    """Validate the player's input."""
    if input_str.isalpha() and len(input_str) == 1:
        if 0 <= ord(input_str.upper()) - 65 < COLUMNS:
            return True
    return False

def drop_checker(board, column, checker):
    """Place a checker in the chosen column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current checker has won the game."""
    # Check horizontal win
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col:col+4] == [checker] * 4:
                return True
    
    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal win (\ direction)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal win (/ direction)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Play the game of Connect 4."""
    board = initialize_board()
    player_turns = [random.choice(range(NUM_PLAYERS))]
    for _ in range(NUM_PLAYERS - 1):
        next_player = (player_turns[-1] + 1) % NUM_PLAYERS
        player_turns.append(next_player)
    
    current_turn = 0

    while True:
        print_board(board)
        player_index = player_turns[current_turn % NUM_PLAYERS]
        player_checker = CHECKERS[player_index]
        player_input = input(f"Player {player_checker}, please enter a column: ").upper()

        if is_valid_input(player_input):
            column_idx = ord(player_input) - 65
            if drop_checker(board, column_idx, player_checker):
                if check_win(board, player_checker):
                    print_board(board)
                    print(f"Player {player_checker} won!")
                    break
                if check_draw(board):
                    print_board(board)
                    print("The game is a draw!")
                    break
                current_turn += 1
            else:
                print("Column is full! Turn skipped.")
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    play_game()
