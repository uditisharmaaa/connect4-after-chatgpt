import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = "ABCDEFG"
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Player tokens

def clear_screen():
    os.system('clear')

def create_board():
    """Creates and returns an empty board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    print(" " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_player_count():
    """Ask for number of players between 2 and 5."""
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Enter an integer between 2 and 5.")

def get_valid_column(board):
    """Prompt player to select a valid column (A-G) which is not full."""
    while True:
        choice = input(f"Choose a column (A-{COLUMN_LABELS[COLUMNS-1]}): ").upper()
        if len(choice) != 1 or choice not in COLUMN_LABELS:
            print("Invalid column. Please enter a valid column letter.")
            continue
        col_index = COLUMN_LABELS.index(choice)
        if board[0][col_index] != ' ':
            print(f"Column {choice} is full. Choose another.")
            continue
        return col_index

def drop_piece(board, col, piece):
    """Drop a piece into the chosen column."""
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = piece
            return row, col

def check_winner(board, piece, row, col):
    """Check all directions if the current move wins the game."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == piece:
            count += 1
            r += dr
            c += dc

        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == piece:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False

def is_draw(board):
    """Returns True if board is full."""
    return all(cell != ' ' for cell in board[0])

def main():
    clear_screen()
    print("=== Connect 4 ===\n")
    player_count = get_player_count()
    players = PLAYERS[:player_count]
    random.shuffle(players)
    print(f"\nPlayers: {' '.join(players)}")
    print(f"{players[0]} goes first!")

    board = create_board()
    current_player_index = 0

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_player_index]

        print(f"\nPlayer {current_player}'s turn.")
        col = get_valid_column(board)
        row, _ = drop_piece(board, col, current_player)

        if check_winner(board, current_player, row, col):
            clear_screen()
            print_board(board)
            print(f"\nPlayer {current_player} wins! Congratulations!\n")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("\nIt's a draw! The board is full.\n")
            break

        current_player_index = (current_player_index + 1) % player_count

if __name__ == "__main__":
    main()
