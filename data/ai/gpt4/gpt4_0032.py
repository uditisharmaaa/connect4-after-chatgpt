import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    """Creates a 2D board with dimensions NUM_ROWS x NUM_COLS."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Prints the game board."""
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(NUM_COLS)))
    print("+---" * NUM_COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLS + "+")

def is_valid_column(column, board):
    """Checks if the chosen column is valid."""
    return column.isalpha() and len(column) == 1 and 'A' <= column.upper() < chr(65 + NUM_COLS) and board[0][ord(column.upper()) - 65] == " "

def drop_checker(column, player, board):
    """Drops the player's checker into the column."""
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = player
            return True
    return False

def check_winner(board, player):
    """Checks if a player has 4 consecutive checkers horizontally, vertically, or diagonally."""
    # Horizontal Check
    for row in board:
        for col in range(NUM_COLS - 3):
            if row[col] == player and row[col + 1] == player and row[col + 2] == player and row[col + 3] == player:
                return True

    # Vertical Check
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Diagonal (\) Check
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Diagonal (/) Check
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

def is_draw(board):
    """Checks if the board is completely filled."""
    return all(board[0][col] != " " for col in range(NUM_COLS))

def main():
    # Initialize game
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)  # Randomly select the first player
    
    while True:
        print_board(board)
        print(f"Player {PLAYER_CHECKERS[current_player]}, it's your turn.")
        
        # Get valid input
        column = input("Please enter a column: ").strip()
        while not is_valid_column(column, board):
            print("Invalid input. Try again.")
            column = input("Please enter a column: ").strip()
        
        # Drop the checker and check for a win/draw
        drop_checker(column, PLAYER_CHECKERS[current_player], board)
        if check_winner(board, PLAYER_CHECKERS[current_player]):
            print_board(board)
            print(f"Player {PLAYER_CHECKERS[current_player]} won!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
