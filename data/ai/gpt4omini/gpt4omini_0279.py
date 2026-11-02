import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the game board."""
    os.system('clear')  # Clear the console (Linux/Unix based)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+---+" + "---+" * (COLS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1))
        
def is_valid_input(col_input):
    """Validates the player's column input."""
    if len(col_input) == 1 and col_input.isalpha():
        col_index = ord(col_input.upper()) - 65
        return 0 <= col_index < COLS
    return False

def drop_checker(board, column, checker):
    """Drops the checker into the specified column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Checks if the specified checker has won the game."""
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

    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-G): ", end="")
        
        while True:
            user_input = input().strip()
            if not is_valid_input(user_input):
                print("Invalid input. Please enter a letter from A to G: ", end="")
                continue

            column = ord(user_input.upper()) - 65
            if drop_checker(board, column, current_player):
                break
            else:
                print("Column is full. Please choose another column: ", end="")

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
