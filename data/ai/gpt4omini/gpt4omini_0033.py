import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # For 2 players

def create_board():
    """Creates a 2D board initialized with spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the board with column labels."""
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input(player):
    """Gets valid column input from the player."""
    while True:
        col_input = input(f"Player {player}, please enter a column: ").upper()
        if len(col_input) == 1 and 'A' <= col_input <= chr(65 + COLS - 1):
            col_index = ord(col_input) - 65
            if board[0][col_index] == " ":
                return col_index
            else:
                print("Column is full. Choose another column.")
        else:
            print("Invalid input. Please enter a letter from A to " + chr(65 + COLS - 1))

def drop_checker(board, col, player):
    """Drops the player's checker in the chosen column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player
            return

def check_win(board, player):
    """Checks for a win condition for the player."""
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                # Check horizontally
                if c + 3 < COLS and all(board[r][c + i] == player for i in range(4)):
                    return True
                # Check vertically
                if r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)):
                    return True
                # Check diagonally (down-right)
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player for i in range(4)):
                    return True
                # Check diagonally (up-right)
                if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == player for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][c] != " " for c in range(COLS))

# Main game function
if __name__ == "__main__":
    board = create_board()
    # Randomly select the first player
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        print_board(board)
        
        current_player = PLAYERS[current_player_index]
        column = get_valid_input(current_player)
        
        drop_checker(board, column, current_player)

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
