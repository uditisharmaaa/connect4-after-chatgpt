import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def clear_screen():
    os.system('clear')  # For Windows use 'cls'

def create_board():
    """Create an empty board as a list of lists filled with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the Connect 4 board with column labels."""
    clear_screen()
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")
    print()

def get_valid_column(board, player):
    """Prompt player for a valid column to drop their piece."""
    while True:
        choice = input(f"Player {player}, choose a column ({'/'.join(COLUMN_LABELS)}): ").upper()
        if choice not in COLUMN_LABELS:
            print(f"Invalid column. Please choose a letter between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.")
            continue
        col = COLUMN_LABELS.index(choice)
        if board[0][col] != ' ':
            print("That column is full. Please pick another one.")
            continue
        return col

def drop_piece(board, col, player):
    """Drop player's piece in the lowest empty row in the chosen column."""
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col  # Return the position where the piece landed

def check_win(board, row, col, player):
    """Check all directions from the last piece for 4 in a row."""
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Count the piece just placed
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc

        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True
    return False

def check_draw(board):
    """Check if the board is full."""
    return all(cell != ' ' for cell in board[0])

def main():
    print("Welcome to Connect 4!")
    # Select number of players
    while True:
        try:
            num_players = int(input(f"Enter number of players (2-{len(PLAYER_SYMBOLS)}): "))
            if 2 <= num_players <= len(PLAYER_SYMBOLS):
                break
            else:
                print(f"Please enter a number between 2 and {len(PLAYER_SYMBOLS)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    players = PLAYER_SYMBOLS[:num_players]

    # Randomly select first player
    current_player_index = random.randint(0, num_players - 1)

    board = create_board()

    while True:
        print_board(board)
        player = players[current_player_index]
        col = get_valid_column(board, player)
        row, col = drop_piece(board, col, player)

        if check_win(board, row, col, player):
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw! No more moves possible.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
