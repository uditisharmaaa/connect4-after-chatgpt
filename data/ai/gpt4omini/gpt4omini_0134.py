import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Extendable to ['X', 'O', 'V', 'H', 'M'] for up to 5 players

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A to G
    print("+---" + "---+---" * (COLS - 1) + "---+")  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Rows
        print("+---" + "---+---" * (COLS - 1) + "---+")  # Row border

def choose_column(player):
    """Prompt player to choose a column."""
    while True:
        column = input(f"Player {player}, please enter a column (A-G): ").upper()
        if column in [chr(65 + i) for i in range(COLS)]:
            return ord(column) - 65  # Convert letter to column index
        else:
            print("Invalid input. Please choose a valid column (A-G).")

def drop_piece(board, column, player):
    """Place a player's piece in the chosen column."""
    for row in reversed(board):  # Check from the bottommost row
        if row[column] == ' ':
            row[column] = player
            return True
    return False  # Column is full

def check_win(board, player):
    """Check for a win condition (horizontal, vertical, diagonal)."""
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

    # Check diagonals (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonals (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    """Main game loop."""
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        column = choose_column(current_player)

        if drop_piece(board, column, current_player):
            print_board(board)

            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break

            if check_draw(board):
                print("The game is a draw!")
                break

            # Switch players
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
        else:
            print("Column is full. Try again.")

if __name__ == "__main__":
    main()
