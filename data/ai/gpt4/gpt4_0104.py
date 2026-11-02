import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Creates an empty board with the specified dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board to the terminal."""
    os.system('clear')  # Clears the terminal screen
    header = "  " + "   ".join(chr(65 + col) for col in range(len(board[0])))
    print(header)
    print("+---" * len(board[0]) + "+")

    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(col, board):
    """Checks if a column is valid and not full."""
    return col in range(COLS) and board[0][col] == " "

def drop_checker(board, col, symbol):
    """Drops a checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row, col

def check_win(board, row, col, symbol):
    """Checks if the current move is a winning move."""

    def check_direction(dx, dy):
        """Check a specific direction for consecutive symbols."""
        count = 0
        for d in range(-3, 4):  # Check range [-3, 3]
            r, c = row + d * dx, col + d * dy
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False

    # Check all directions
    return (
        check_direction(1, 0) or  # Vertical
        check_direction(0, 1) or  # Horizontal
        check_direction(1, 1) or  # Diagonal down-right
        check_direction(1, -1)    # Diagonal down-left
    )

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLS))

def get_player_move(players, current_player, board):
    """Gets a valid move from the current player."""
    while True:
        column_input = input(f"Player {players[current_player]}, please enter a column: ").strip().upper()
        
        # Ensure only single letter input
        if len(column_input) != 1:
            print("Invalid input. Please enter a single letter (A-G).")
            continue

        col = ord(column_input) - 65  # Convert letter to column index
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(64 + COLS)}.")
        elif not is_valid_column(col, board):
            print("This column is full. Choose another one.")
        else:
            return col

def play_game():
    """Main function to play the Connect 4 game."""
    os.system('clear')
    print("Welcome to Connect 4!\n")

    # Initialize board and players
    board = create_board(ROWS, COLS)
    num_players = 2
    players = PLAYER_SYMBOLS[:num_players]

    # Choose a random first player
    current_player = random.randint(0, num_players - 1)

    print_board(board)

    # Game loop
    while True:
        print(f"Player {players[current_player]}'s turn!")
        col = get_player_move(players, current_player, board)
        row, col = drop_checker(board, col, players[current_player])
        print_board(board)

        # Check for win
        if check_win(board, row, col, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Switch player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    play_game()
