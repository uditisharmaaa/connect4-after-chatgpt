import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Allow up to 5 players

def create_board():
    """Create and return an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Clear the screen and print the current game board."""
    os.system('clear')  # Clear console screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_current_player_index(turn, num_players):
    """Get the current player's index based on turn and number of players."""
    return turn % num_players

def is_valid_input(col_input, board):
    """Check if the input column (A-G) is valid and the column is not full."""
    if len(col_input) != 1 or not col_input.isalpha():
        return False
    col_index = ord(col_input.upper()) - 65
    return 0 <= col_index < COLS and board[0][col_index] == " "

def place_checker(board, col_index, player_symbol):
    """Place a checker in the board at the specified column index."""
    for row in reversed(range(ROWS)):
        if board[row][col_index] == " ":
            board[row][col_index] = player_symbol
            break

def check_winner(board, player_symbol):
    """Check if the current player has four checkers in a row."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player_symbol for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True

    # Check diagonal (/) 
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True

    # Check diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full with no winner."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    num_players = min(len(PLAYERS), 5)  # Up to 5 players
    current_player_index = random.randint(0, num_players - 1)  # Random starting player
    turn = 0

    while True:
        print_board(board)
        player_symbol = PLAYERS[current_player_index]
        col_input = input(f"Player {player_symbol}, please enter a column (A-G): ").upper()

        # Validate input before placing the checker
        while not is_valid_input(col_input, board):
            col_input = input(f"Invalid input. Player {player_symbol}, please enter a column (A-G): ").upper()

        col_index = ord(col_input) - 65
        place_checker(board, col_index, player_symbol)

        # Check for a winner
        if check_winner(board, player_symbol):
            print_board(board)
            print(f"Player {player_symbol} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players
        turn += 1

# Run the game
if __name__ == "__main__":
    main()
