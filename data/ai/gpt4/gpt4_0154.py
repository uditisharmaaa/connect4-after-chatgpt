import os
import random

# Constants for game configuration
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Symbols for 2 to 5 players
NUM_PLAYERS = 2  # Number of players

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates an empty game board with the specified dimensions."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the game board."""
    clear_screen()
    # Print column labels
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    """Checks if the column is valid and has available space."""
    if column < 0 or column >= COLUMNS:
        return False
    return board[0][column] == " "

def drop_checker(board, column, symbol):
    """Drops a checker into the lowest available space in the chosen column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = symbol
            return

def check_winner(board, symbol):
    """Checks if the given player symbol has won the game."""
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True
    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True
    # Check diagonal win (/ direction)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True
    # Check diagonal win (\ direction)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True
    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def get_column_input():
    """Gets a valid column input from the player."""
    while True:
        user_input = input("Please enter a column (A-G): ").upper()
        if len(user_input) == 1 and 'A' <= user_input <= chr(ord('A') + COLUMNS - 1):
            return ord(user_input) - ord('A')
        else:
            print("Invalid input. Please enter a valid column letter.")

def play_game():
    """Main function to play the Connect 4 game."""
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    random.shuffle(players)  # Shuffle to determine the first player
    current_player_index = 0

    print_board(board)
    print(f"Player {players[current_player_index]} goes first!")

    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn.")
        while True:
            column = get_column_input()
            if is_valid_column(column, board):
                drop_checker(board, column, current_player)
                break
            else:
                print("Column is full or invalid. Try again.")

        print_board(board)

        # Check for win or draw
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
