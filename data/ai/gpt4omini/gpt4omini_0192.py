import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def create_board():
    """Create a 2D board initialized with spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+---" + "---+" * (COLS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLS - 1) + "---+")

def is_valid_input(column, board):
    """Check if the input column is valid."""
    return column.isalpha() and len(column) == 1 and 'A' <= column.upper() <= chr(ord('A') + COLS - 1) and board[0][ord(column.upper()) - ord('A')] == " "

def drop_checker(board, column, player):
    """Drop the player's checker into the selected column."""
    col_index = ord(column.upper()) - ord('A')
    for row in reversed(board):  # Start from the bottom of the column
        if row[col_index] == " ":
            row[col_index] = player
            return True
    return False

def check_win(board, player):
    """Check for a win for the given player."""
    # Check horizontal, vertical and diagonal wins
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                # Check right
                if c + 3 < COLS and all(board[r][c + i] == player for i in range(4)):
                    return True
                # Check down
                if r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)):
                    return True
                # Check diagonal right-down
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player for i in range(4)):
                    return True
                # Check diagonal left-down
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == player for i in range(4)):
                    return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[0][c] != " " for c in range(COLS))

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    game_over = False

    while not game_over:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        column = input(f"Player {current_player}, please enter a column: ")

        while not is_valid_input(column, board):
            print("Invalid input. Please try again.")
            column = input(f"Player {current_player}, please enter a column: ")

        if drop_checker(board, column, current_player):
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                game_over = True
            elif is_draw(board):
                print_board(board)
                print("The game is a draw!")
                game_over = True
            else:
                current_player_index = (current_player_index + 1) % len(PLAYERS)  # Next player
        else:
            print("Column is full. Try a different column.")

if __name__ == "__main__":
    main()
