import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players

def create_board():
    """Create and initialize the board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Clear the screen and print the current board state."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Print column labels A to G
    print("+---" * COLS + "+")
    for row in board:  # Print each row of the board
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_input(column, board):
    """Check if the given column input is valid."""
    if column < 0 or column >= COLS or board[0][column] != ' ':
        return False
    return True

def place_checker(board, column, player):
    """Place the player's checker in the specified column."""
    for row in reversed(board):  # Place the checker in the lowest empty position
        if row[column] == ' ':
            row[column] = player
            return True
    return False

def check_winner(board, player):
    """Check if the given player has won the game."""
    # Check horizontal, vertical, and diagonal lines for a win
    for row in range(ROWS):
        for col in range(COLS):
            # Check horizontal
            if col + 3 < COLS and all(board[row][col + i] == player for i in range(4)):
                return True
            # Check vertical
            if row + 3 < ROWS and all(board[row + i][col] == player for i in range(4)):
                return True
            # Check diagonal (bottom-left to top-right)
            if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == player for i in range(4)):
                return True
            # Check diagonal (top-left to bottom-right)
            if row - 3 >= 0 and col + 3 < COLS and all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()  # Create the board
    current_player_index = random.randint(0, len(PLAYERS) - 1)  # Randomize starting player
    game_over = False

    print_board(board)  # Print the initial empty board

    while not game_over:
        current_player = PLAYERS[current_player_index]
        # Prompt the current player for input
        while True:
            try:
                column_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
                if len(column_input) != 1 or not column_input.isalpha():
                    raise ValueError("Invalid input, please enter a letter.")
                column = ord(column_input) - 65  # Convert column letter to index
                if is_valid_input(column, board):
                    break  # Valid input, exit the loop
                else:
                    print("Invalid column! Please choose another column.")
            except ValueError as e:
                print(e)

        if place_checker(board, column, current_player):
            print_board(board)  # Update the board after placing the checker
            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                game_over = True
            elif is_draw(board):
                print("The game is a draw!")
                game_over = True
            current_player_index = (current_player_index + 1) % len(PLAYERS)  # Switch to the next player

if __name__ == "__main__":
    main()
