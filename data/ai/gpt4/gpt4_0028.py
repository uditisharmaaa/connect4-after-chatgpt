import os
import random

# Constants for the game
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates an empty game board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    header = "  " + "   ".join([chr(65 + col) for col in range(len(board[0]))])
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    """Checks if the column selection is valid."""
    if column < 0 or column >= len(board[0]):
        return False
    return board[0][column] == " "

def get_lowest_row(column, board):
    """Gets the lowest available row in the selected column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            return row
    return None

def check_winner(board, checker, row, col):
    """Checks for a win condition for a specific checker at (row, col)."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal /
        (1, -1)  # Diagonal \
    ]
    for dr, dc in directions:
        count = 1
        for i in [1, -1]:  # Extend in both directions
            r, c = row + dr * i, col + dc * i
            while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
                count += 1
                r += dr * i
                c += dc * i
            if count >= 4:
                return True
    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(len(board[0])))

def get_column_input(num_cols):
    """Gets validated column input from the player."""
    while True:
        try:
            col_input = input("Please enter a column (A-G): ").strip().upper()
            if len(col_input) == 1 and "A" <= col_input <= chr(64 + num_cols):
                return ord(col_input) - 65
        except ValueError:
            pass
        print("Invalid input. Please try again.")

def switch_turn(player_turn, total_players):
    """Switches the turn to the next player."""
    return (player_turn + 1) % total_players

def play_game():
    """Main game loop."""
    # Create the board and initialize variables
    board = create_board(NUM_ROWS, NUM_COLS)
    num_players = 2  # Set number of players; can be modified for other scenarios
    players = PLAYER_CHECKERS[:num_players]
    current_player = random.randint(0, num_players - 1)

    clear_screen()
    print_board(board)

    while True:
        print(f"Player {players[current_player]}'s turn!")
        col = get_column_input(NUM_COLS)

        # Check if the selected column is valid
        if not is_valid_column(col, board):
            print("Column is full or invalid. Try again.")
            continue

        # Place the checker in the board
        row = get_lowest_row(col, board)
        board[row][col] = players[current_player]

        clear_screen()
        print_board(board)

        # Check for win condition
        if check_winner(board, players[current_player], row, col):
            print(f"Player {players[current_player]} won!")
            break

        # Check for draw condition
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = switch_turn(current_player, num_players)

if __name__ == "__main__":
    play_game()
