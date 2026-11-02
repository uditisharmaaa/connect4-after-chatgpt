import os
import random

# Constants for the game
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # player pieces
MIN_PLAYERS = 2
MAX_PLAYERS = 5

def clear_screen():
    """Clears the console screen."""
    os.system('clear')

def create_board():
    """Creates an empty board as 2D list filled with '.' to represent empty slots."""
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the board with column labels."""
    print(' ' + ' '.join(COLUMN_LABELS))  # print columns header
    for row in board:
        print(' ' + ' '.join(row))
    print()  # extra newline for spacing

def get_player_count():
    """Prompts user to enter number of players between MIN_PLAYERS and MAX_PLAYERS."""
    while True:
        try:
            count = int(input(f"Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= count <= MAX_PLAYERS:
                return count
            else:
                print(f"Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Please enter a valid integer.")

def get_valid_column(board, player):
    """Prompts current player to select a valid column that is not full."""
    while True:
        choice = input(f"Player {player}, choose a column (A-G): ").upper()
        if choice in COLUMN_LABELS:
            col_index = COLUMN_LABELS.index(choice)
            # check if top slot is empty to allow a new piece
            if board[0][col_index] == '.':
                return col_index
            else:
                print(f"Column {choice} is full. Choose another one.")
        else:
            print("Invalid column. Please enter a letter from A to G.")

def drop_piece(board, col, player):
    """Drops the player's piece into the selected column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == '.':
            board[row][col] = player
            return row, col  # return position where piece landed

def check_winner(board, row, col, player):
    """Check if placing a piece at (row, col) causes player to win."""

    def count_direction(dr, dc):
        """Count continuous pieces of the player in one direction."""
        r, c = row + dr, col + dc
        count = 0
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        return count

    # Directions to check: horizontal, vertical, diagonal /
    directions = [
        ((0, 1), (0, -1)),  # horizontal (right, left)
        ((1, 0), (-1, 0)),  # vertical (down, up)
        ((1, 1), (-1, -1)), # diagonal down-right & up-left
        ((1, -1), (-1, 1))  # diagonal down-left & up-right
    ]

    for dir1, dir2 in directions:
        count = 1  # start with current spot
        count += count_direction(*dir1)
        count += count_direction(*dir2)
        if count >= 4:
            return True
    return False

def check_draw(board):
    """Check if the board is full - no '.' left."""
    return all(board[0][col] != '.' for col in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!\n")

    num_players = get_player_count()
    players = PLAYERS[:num_players]

    # Pick random player to start
    current_index = random.randint(0, num_players - 1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        player = players[current_index]

        col = get_valid_column(board, player)
        row, col = drop_piece(board, col, player)

        # Check for a win
        if check_winner(board, row, col, player):
            clear_screen()
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break

        # Check for a draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! Board is full.")
            break

        # Move to next player
        current_index = (current_index + 1) % num_players

if __name__ == "__main__":
    main()
