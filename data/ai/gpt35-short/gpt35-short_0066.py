import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players

# Number of players for this game (change this constant for different player counts)
NUM_PLAYERS = 3  # must be between 2 and 5 inclusive

# Validate number of players
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    raise ValueError("NUM_PLAYERS must be between 2 and 5")

# Only use the first NUM_PLAYERS from PLAYERS list
players = PLAYERS[:NUM_PLAYERS]

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear')

def create_board():
    """Create a blank board"""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels"""
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (2 * COLS + 1))

def get_column_index(choice):
    """Convert column letter to index (0-based)"""
    choice = choice.upper()
    if choice in COLUMN_LABELS:
        return COLUMN_LABELS.index(choice)
    return -1

def is_valid_move(board, col):
    """Check if a move is valid (if column is not full)"""
    return board[0][col] == ' '

def make_move(board, col, player):
    """Place player's token in the chosen column, returns row where token lands"""
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1  # should never happen if move is validated before

def check_win(board, row, col, player):
    """Check all directions for a win starting from last placed token"""

    def count_direction(dr, dc):
        """Count continuous tokens of same player in one direction"""
        r, c = row + dr, col + dc
        count = 0
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        return count

    # Check horizontal (left + right)
    horizontal = 1 + count_direction(0, -1) + count_direction(0, 1)
    if horizontal >= 4:
        return True
    # Check vertical (down + up)
    vertical = 1 + count_direction(-1, 0) + count_direction(1, 0)
    if vertical >= 4:
        return True
    # Check diagonal1 (\ direction)
    diag1 = 1 + count_direction(-1, -1) + count_direction(1, 1)
    if diag1 >= 4:
        return True
    # Check diagonal2 (/ direction)
    diag2 = 1 + count_direction(-1, 1) + count_direction(1, -1)
    if diag2 >= 4:
        return True

    return False

def board_full(board):
    """Check if the board is full resulting in a draw"""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print(f"Welcome to Connect 4! Players: {', '.join(players)}")
    print(f"Starting player randomly chosen: {players[current_player_idx]}")
    
    while True:
        print_board(board)

        # Prompt current player for their move
        player = players[current_player_idx]
        move = input(f"Player {player}, choose a column (A-G): ").strip().upper()

        col = get_column_index(move)

        if col == -1:
            clear_screen()
            print(f"Invalid column '{move}'. Please choose a column between A and G.")
            continue

        if not is_valid_move(board, col):
            clear_screen()
            print(f"Column '{move}' is full. Please choose a different column.")
            continue

        # Make move
        row = make_move(board, col, player)
        clear_screen()

        # Check win
        if check_win(board, row, col, player):
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break

        # Check draw
        if board_full(board):
            print_board(board)
            print("The game is a draw! No more moves available.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
