import os
import random

# Constants for board dimensions and player checkers
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    """Create a new game board initialized with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels
    print("+---" + "---+" * (COLS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLS - 1) + "---+")
        
def make_move(board, column, player):
    """Place the player's checker in the desired column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return True
    return False  # Column is full

def is_winner(board, player):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    # Initialize the game
    board = create_board()
    num_players = min(len(PLAYERS), 5)  # Limit to max 5 players
    current_player_index = random.randint(0, num_players - 1)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        
        # Prompt the current player for input
        while True:
            column_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
            if column_input in [chr(65 + i) for i in range(COLS)]:
                column = ord(column_input) - 65
                if make_move(board, column, current_player):
                    break
                else:
                    print("Column is full! Try again.")
            else:
                print("Invalid input! Please enter a valid column (A-G).")

        if is_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
