import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return a new Connect 4 board initialized with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input(player):
    """Prompt the player for a valid column input, returning the letter corresponding to the column."""
    while True:
        inp = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if len(inp) == 1 and 'A' <= inp <= chr(65 + COLS - 1):
            col = ord(inp) - 65
            if board[0][col] == ' ':
                return col
            else:
                print("Column is full, please choose another column.")
        else:
            print("Invalid input. Please enter a column letter (A-G).")

def drop_checker(board, column, player):
    """Drop the player's checker into the specified column on the board."""
    for row in reversed(range(ROWS)):
        if board[row][column] == ' ':
            board[row][column] = player
            return

def check_winner(board, player):
    """Check for a win condition for the specified player."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full indicating a draw."""
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    """Main game loop."""
    board = create_board()
    current_player = random.choice(PLAYERS)

    while True:
        print_board(board)
        col = get_valid_input(current_player)
        drop_checker(board, col, current_player)

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch player
        current_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_index + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
