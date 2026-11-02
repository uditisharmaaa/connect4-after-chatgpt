import os
import random

# Constants for the game setup
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')  # For Windows change to 'cls' if needed

def create_board():
    """Create an empty board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Display the board with column labels."""
    clear_screen()
    # Print column labels
    print(' ' + '   '.join(COLUMN_LABELS))
    # Print rows of the board
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('-' * (COLUMNS * 4 + 1))  # Board bottom border

def get_valid_column(board, player):
    """Prompt the player for a valid column to drop a disc."""
    while True:
        col_input = input(f"Player {player}, choose a column (A-G): ").strip().upper()
        if col_input not in COLUMN_LABELS:
            print("Invalid column. Please choose a letter from A to G.")
            continue

        col = COLUMN_LABELS.index(col_input)
        # Check if the column is not full
        if board[0][col] != ' ':
            print("Column is full. Choose another column.")
            continue

        return col

def drop_disc(board, col, player):
    """Place the player's disc in the specified column."""
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col  # Return the position where the disc landed

def check_winner(board, row, col, player):
    """Check if placing a disc at (row, col) causes player to win."""

    def count_direction(dr, dc):
        """Count consecutive discs for player in direction (dr, dc) starting from (row, col)."""
        r, c = row + dr, col + dc
        count = 0
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        return count

    # Directions: horizontal, vertical, diagonal /
    directions = [(0,1), (1,0), (1,1), (1,-1)]

    for dr, dc in directions:
        # Count discs in positive and negative direction and add 1 for current spot
        total = 1 + count_direction(dr, dc) + count_direction(-dr, -dc)
        if total >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full with no winner (draw)."""
    return all(cell != ' ' for cell in board[0])  # Top row has no empty spaces

def main():
    """Main game loop."""
    # Ask number of players between 2 and 5
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            print("Number of players must be between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number between 2 and 5.")

    players = PLAYERS[:num_players]

    # Randomly pick the first player
    current_idx = random.randint(0, num_players -1)
    board = create_board()

    while True:
        print_board(board)
        current_player = players[current_idx]

        col = get_valid_column(board, current_player)
        row, col = drop_disc(board, col, current_player)

        if check_winner(board, row, col, current_player):
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        # Move to next player
        current_idx = (current_idx + 1) % num_players

if __name__ == "__main__":
    main()
