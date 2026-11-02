import os
import random

# Constants for the game
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']  # Column labels A-G

# Available player marks
PLAYER_MARKS = ['X', 'O', 'V', 'H', 'M']  

def clear_screen():
    """Clear terminal screen."""
    os.system('clear')

def create_board():
    """Create and return an empty board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels."""
    print("  " + " ".join(COL_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))  # Bottom border

def get_move(player, used_cols):
    """
    Prompt the current player to choose a column to drop their piece into.
    Validate the input to ensure it's in A-G and the column is not full.
    """
    while True:
        move = input(f"Player {player}'s turn. Choose column (A-G): ").upper()
        if move not in COL_LABELS:
            print("Invalid column. Choose a letter from A to G.")
            continue
        col = COL_LABELS.index(move)
        if used_cols[col] >= ROWS:
            print(f"Column {move} is full. Choose another column.")
            continue
        return col

def drop_piece(board, col, piece, used_cols):
    """Place the piece in the lowest available row in the selected column."""
    row = ROWS - 1 - used_cols[col]  # Calculate the next available row from bottom
    board[row][col] = piece
    used_cols[col] += 1
    return row, col

def check_win(board, piece, row, col):
    """
    Check all directions (horizontal, vertical, diagonal) for 4 in a row.
    Only need to check from the last placed piece for efficiency.
    """

    def count_dir(dr, dc):
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == piece:
            count += 1
            r += dr
            c += dc
        return count

    # Directions: horizontal, vertical, diagonal up-right, diagonal down-right
    directions = [(0,1), (1,0), (1,1), (1,-1)]

    for dr, dc in directions:
        # count pieces of current player in positive and negative directions
        count = 1  # counting the last placed piece itself
        count += count_dir(dr, dc)
        count += count_dir(-dr, -dc)
        if count >= 4:
            return True
    return False

def check_draw(used_cols):
    """Check if the board is full (draw)."""
    return all(used == ROWS for used in used_cols)

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    # Get number of players
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            print("Number of players must be between 2 and 5.")
        except ValueError:
            print("Please enter a valid number.")

    players = PLAYER_MARKS[:num_players]
    used_cols = [0] * COLS  # Track how many pieces in each column

    # Randomly choose first player index
    current_player_index = random.randint(0, num_players -1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_player_index]

        # Get a validated move from the current player
        col = get_move(current_player, used_cols)

        # Drop the piece and get the row where it landed
        row, col = drop_piece(board, col, current_player, used_cols)

        # Check for win
        if check_win(board, current_player, row, col):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        # Check for draw
        if check_draw(used_cols):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        # Move to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
