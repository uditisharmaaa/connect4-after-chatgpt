import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Maximum 5 players allowed
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # Labels A, B, C, ...

def clear_screen():
    """Clears the terminal."""
    os.system('clear')

def create_board():
    """Creates an empty board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the board to the terminal."""
    clear_screen()
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column_input):
    """Checks if the user input for column is valid."""
    return column_input in COLUMN_LABELS

def get_column_index(column_input):
    """Maps column label to its index."""
    return COLUMN_LABELS.index(column_input)

def is_column_full(board, column):
    """Checks if a column is full."""
    return board[0][column] != " "

def drop_checker(board, column, checker):
    """Drops the checker into the correct location in the column."""
    for row in range(ROWS - 1, -1, -1):  # Start from bottom row
        if board[row][column] == " ":
            board[row][column] = checker
            return row, column  # Return the position of the placed checker

def check_winner(board, row, col, checker):
    """Checks if placing the checker caused a win."""
    directions = [
        [(0, 1), (0, -1)],  # Horizontal
        [(1, 0), (-1, 0)],  # Vertical
        [(1, 1), (-1, -1)],  # Diagonal /
        [(1, -1), (-1, 1)]   # Diagonal \
    ]
    for direction in directions:
        count = 1  # Start with the placed checker
        for dx, dy in direction:
            r, c = row, col
            while True:
                r += dx
                c += dy
                if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                    count += 1
                    if count == 4:  # Found 4 in a row
                        return True
                else:
                    break
    return False

def is_draw(board):
    """Checks if the board is full, resulting in a draw."""
    return all(is_column_full(board, col) for col in range(COLUMNS))

def play_game():
    """Implements the Connect 4 game logic."""
    # Initialization
    board = create_board()
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player = random.choice(players)
    
    print_board(board)
    print(f"Randomly selected first player: {current_player}")

    while True:
        # Prompt current player for input
        player_input = input(f"Player {current_player}, please enter a column: ").strip().upper()

        # Input validation
        if not is_valid_column(player_input):
            print("Invalid column. Please enter a valid column letter.")
            continue

        column_index = get_column_index(player_input)

        if is_column_full(board, column_index):
            print(f"Column {player_input} is full. Please select a different column.")
            continue

        # Place the checker
        row, col = drop_checker(board, column_index, current_player)
        print_board(board)

        # Check for win
        if check_winner(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    play_game()
