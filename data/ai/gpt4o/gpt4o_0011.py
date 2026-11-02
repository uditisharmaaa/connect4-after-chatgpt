import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2

# Player markers
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates a game board with dimensions ROWS x COLUMNS."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the game board."""
    os.system('clear')  # Clear the game screen before printing the updated board
    column_labels = ' '.join(chr(ord('A') + i) for i in range(COLUMNS))
    print(f"  {column_labels}")
    print("+---" * COLUMNS + "+")

    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_valid_column(board, current_player):
    """Prompts player for a valid column and returns the column index."""
    while True:
        col_input = input(f"Player {PLAYER_MARKERS[current_player]}, please enter a column: ").strip().upper()
        if len(col_input) == 1 and 'A' <= col_input <= chr(ord('A') + COLUMNS - 1):
            col = ord(col_input) - ord('A')
            if board[0][col] == ' ':
                return col
        print("Invalid input. Please enter a valid column.")

def place_checker(board, col, current_player):
    """Places the checker in the specified column for the current player."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = PLAYER_MARKERS[current_player]
            return row, col

def check_winner(board, row, col, player_marker):
    """Checks for a win condition from the specified position."""
    def count_checkers(direction):
        dr, dc = direction
        r, c = row + dr, col + dc
        count = 0
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_marker:
            count += 1
            r += dr
            c += dc
        return count

    # Directions: horizontal (right), vertical (down), diagonal (up-right), diagonal (down-right)
    directions = [(0, 1), (1, 0), (-1, 1), (1, 1)]

    for dr, dc in directions:
        if count_checkers((dr, dc)) + count_checkers((-dr, -dc)) >= 3:
            return True
    return False

def check_draw(board):
    """Checks if the board is full, indicating a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def connect_4_game():
    """Runs a Connect 4 game."""
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        col = get_valid_column(board, current_player)
        row, col = place_checker(board, col, current_player)
        print_board(board)

        if check_winner(board, row, col, PLAYER_MARKERS[current_player]):
            print(f"Player {PLAYER_MARKERS[current_player]} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    connect_4_game()
