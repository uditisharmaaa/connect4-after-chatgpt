import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]  # Checker symbols for up to 5 players
NUM_PLAYERS = 2  # Set to 2 players (you can change it up to MAX_PLAYERS)

def create_board():
    """Creates an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')
    # Print the column labels (A, B, C, ...)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_column_input(player):
    """Gets valid column input from the player."""
    while True:
        try:
            column = input(f"Player {player}, please enter a column: ").strip().upper()
            if len(column) != 1 or not ('A' <= column <= chr(65 + COLS - 1)):
                raise ValueError("Invalid column. Please enter a valid column letter.")
            col_index = ord(column) - 65
            return col_index
        except ValueError as e:
            print(e)

def place_checker(board, col, player):
    """Places the player's checker in the specified column."""
    for row in reversed(board):  # Start from bottom-most row
        if row[col] == " ":
            row[col] = player
            return True
    return False  # Column is full

def check_winner(board, player):
    """Checks if the player has won the game."""
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check vertically
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonally (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonally (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    # Initialize the board and choose the players
    board = create_board()
    players = PLAYERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)  # Randomly choose the starting player

    print_board(board)

    # Game loop
    while True:
        current_player = players[current_player_index]
        print(f"It's Player {current_player}'s turn.")
        
        # Get valid column input and place the checker
        while True:
            col = get_column_input(current_player)
            if place_checker(board, col, current_player):
                break
            print("Column is full. Choose another column.")

        # Print the updated board
        print_board(board)

        # Check if the current player wins
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check if the game is a draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
