import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # For the assignment, set to 2 players only

def create_board():
    """Create the Connect 4 game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current game board."""
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def is_valid_input(column):
    """Check if the input is valid."""
    return column in range(COLS)

def drop_checker(board, column, checker):
    """Drop a checker into the selected column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_winner(board, checker):
    """Check if the current player has won."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = random.choice(PLAYERS)
    game_over = False

    print_board(board)

    while not game_over:
        print(f"Player {current_player}, please enter a column (A-G): ")
        column_input = input().strip().upper()

        if column_input in [chr(ord('A') + i) for i in range(COLS)]:
            column = ord(column_input) - ord('A')
            if drop_checker(board, column, current_player):
                print_board(board)
                if check_winner(board, current_player):
                    print(f"Player {current_player} won!")
                    game_over = True
                elif is_draw(board):
                    print("The game is a draw!")
                    game_over = True
                current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
            else:
                print("Column is full, please choose a different column.")
        else:
            print("Invalid input. Please enter a letter between A and G.")

if __name__ == "__main__":
    main()
