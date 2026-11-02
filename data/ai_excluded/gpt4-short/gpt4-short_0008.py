import random
import os

# Constants for players and board size
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Symbols for players
NUM_PLAYERS = 2  # Can be set to any number from 2 to 5
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def initialize_board():
    """Creates an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board."""
    clear_screen()
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("| " + " ".join(row) + " |")
    print("  " + "-" * (2 * COLS - 1))

def is_valid_column(col, board):
    """Checks if a column is valid for a move."""
    return 0 <= col < COLS and board[0][col] == ' '

def drop_piece(board, col, player):
    """Drops a piece for the player in the chosen column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def is_winner(board, row, col, player):
    """Checks if the given player has won."""
    def count_direction(dx, dy):
        count = 0
        r, c = row + dx, col + dy
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dx
            c += dy
        return count

    # Check all 4 directions: horizontal, vertical, diagonal-down, diagonal-up
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        if 1 + count_direction(dx, dy) + count_direction(-dx, -dy) >= 4:
            return True
    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLS))

def get_player_input(current_player, board):
    """Gets a valid column input from the current player."""
    while True:
        try:
            move = input(f"{current_player}'s turn. Choose a column (A-G): ").upper()
            if move not in COLUMN_LABELS:
                raise ValueError("Invalid column. Please choose from A-G.")
            col = COLUMN_LABELS.index(move)
            if not is_valid_column(col, board):
                raise ValueError("Column is full. Choose another.")
            return col
        except ValueError as e:
            print(e)

def play_connect4():
    """Main function to play Connect 4."""
    board = initialize_board()
    players = PLAYERS[:NUM_PLAYERS]
    random.shuffle(players)  # Randomize player order
    clear_screen()
    print(f"Player order: {', '.join(players)}")
    input("Press Enter to start the game...")

    turn = 0
    while True:
        print_board(board)
        current_player = players[turn % NUM_PLAYERS]
        col = get_player_input(current_player, board)
        row, col = drop_piece(board, col, current_player)

        if is_winner(board, row, col, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        turn += 1

if __name__ == "__main__":
    play_connect4()
