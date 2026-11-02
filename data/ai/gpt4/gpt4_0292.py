import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def initialize_board():
    """Creates and initializes the game board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    print("  " + "   ".join([chr(65 + col) for col in range(COLUMNS)]))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    """Checks if the chosen column is valid for placing a checker."""
    if column < 0 or column >= COLUMNS:
        return False
    return board[0][column] == " "

def get_column_input(board):
    """Prompts the user until a valid column is selected."""
    while True:
        user_input = input("Please enter a column (A-G): ").upper()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Enter a letter matching an available column.")
            continue

        column = ord(user_input) - 65

        if is_valid_column(column, board):
            return column
        print("Invalid or full column. Choose another.")

def place_checker(column, player, board):
    """Places the checker for a given player at the correct position."""
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = player
            return row

def check_victory(row, col, board, player):
    """Checks whether the player has won the game."""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for i in range(1, 4):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
                count += 1
            else:
                break
        for i in range(1, 4):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
                count += 1
            else:
                break
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Checks if the board is full (i.e., the game is a draw)."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    """Main function to play Connect 4."""
    # Initialize the game
    board = initialize_board()
    num_players = 2  # 2 players for the assignment; can be between 2 and 5
    players = CHECKERS[:num_players]

    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    current_player = players[current_player_index]

    # Game loop
    while True:
        clear_screen()
        print_board(board)
        print(f"Player {current_player}, it's your turn.")
        
        column = get_column_input(board)
        row = place_checker(column, current_player, board)

        # Check for win or draw
        if check_victory(row, column, board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players
        current_player = players[current_player_index]

if __name__ == "__main__":
    main()
