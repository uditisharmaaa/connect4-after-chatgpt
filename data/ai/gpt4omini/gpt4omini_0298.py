import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players

def create_board():
    """Creates an empty Connect 4 board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the terminal for a fresh board display
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "+---" * (COLS - 1) + "+")
    # Print each row of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def is_valid_column(column):
    """Checks if a column input is valid (A-G)."""
    return len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1)

def find_lowest_empty_row(board, column):
    """Finds the lowest empty row in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            return row
    return -1  # Column is full

def check_win(board, player):
    """Checks if the current player has four in a row."""
    # Check horizontal, vertical and diagonal placements for a win
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                if c + 3 < COLS and all(board[r][c+i] == player for i in range(4)):
                    return True  # Horizontal
                if r + 3 < ROWS and all(board[r+i][c] == player for i in range(4)):
                    return True  # Vertical
                if r + 3 < ROWS and c + 3 < COLS and all(board[r+i][c+i] == player for i in range(4)):
                    return True  # Diagonal /
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r+i][c-i] == player for i in range(4)):
                    return True  # Diagonal \
    return False

def check_draw(board):
    """Checks if the game is a draw (no empty spaces left)."""
    return all(cell != ' ' for row in board for cell in row)

def connect_4_game():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = random.choice(PLAYERS)  # Randomly select the first player
    total_players = len(PLAYERS)
    game_over = False

    while not game_over:
        print_board(board)  # Print the current state of the board
        print(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}):")

        while True:
            column_input = input().strip().upper()
            if is_valid_column(column_input):
                column_index = ord(column_input) - 65
                row_index = find_lowest_empty_row(board, column_index)

                if row_index != -1:  # Valid place to drop the checker
                    board[row_index][column_index] = current_player
                    break
                else:
                    print("Column is full! Please choose another column.")
            else:
                print("Invalid input! Please enter a valid column (A-G).")

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % total_players]

if __name__ == "__main__":
    connect_4_game()
