import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')  # Use 'cls' if on Windows

def create_board():
    """Create an empty board represented by a 2D list."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the Connect 4 board with column labels."""
    # Print column labels
    print('  ' + ' '.join(COLUMN_LABELS))
    # Print each row
    for row in board:
        print('|'+ '|'.join(row) + '|')
    print('-' * (COLS * 2 + 1))  # bottom border

def get_valid_column(board, current_player):
    """
    Prompt the current player to input a column letter.
    Validate that it is within A-G and that the column is not full.
    """
    while True:
        col_input = input(f"Player {current_player} choose a column (A-G): ").upper()
        if col_input not in COLUMN_LABELS:
            print(f"Invalid input '{col_input}'. Please enter a letter from A to G.")
            continue
        col_index = COLUMN_LABELS.index(col_input)
        if board[0][col_index] != ' ':
            print(f"Column {col_input} is full. Choose another column.")
            continue
        return col_index

def drop_piece(board, col, player):
    """
    Drop the player's piece into the selected column.
    Pieces fall to the lowest empty cell in the column.
    """
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col  # Return the position where the piece landed

def check_win(board, row, col, player):
    """
    Check all directions from the last placed piece to see if player won.
    Return True if player has 4 in a row.
    """
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Count the current piece

        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc

        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False

def board_full(board):
    """Check if the board is full (draw condition)."""
    return all(cell != ' ' for cell in board[0])

def main():
    clear_screen()

    print("Welcome to Connect 4!")
    # Get number of players
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Please enter a number from 2 to 5.")
        except ValueError:
            print("Invalid input, please enter a number.")

    players = PLAYER_SYMBOLS[:num_players]

    # Choose a random first player
    current_index = random.randint(0, num_players - 1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_index]
        print(f"Player {current_player}'s turn")

        # Get a valid column index from the player
        col = get_valid_column(board, current_player)

        # Drop the piece and get the position where it landed
        row, col = drop_piece(board, col, current_player)

        # Check if current player won
        if check_win(board, row, col, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Move to next player
        current_index = (current_index + 1) % num_players

if __name__ == "__main__":
    main()
