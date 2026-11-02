import os
import random
import string

# === CONSTANTS ===
ROWS = 6
COLS = 7
MAX_COLS = 26  # So we don't exceed the alphabet
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

# === FUNCTION DEFINITIONS ===

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Create the board as a list of lists filled with ' ' (whitespace)."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """Print the board to the terminal with proper formatting."""
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("\n  " + "   ".join(col_labels))
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_player_input(player_checker, cols):
    """Prompt the player for a valid move and return the column index."""
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        move = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(move) != 1 or move not in col_labels:
            print(f"Invalid input. Enter a column letter between A and {col_labels[-1]}.")
            continue
        # Return the column index
        return col_labels.index(move)

def drop_checker(board, col, player_checker):
    """
    Drop a checker into the specified column.
    Returns True if successful, False if column is full.
    """
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player_checker
            return True
    return False  # Column full

def is_board_full(board):
    """Return True if the board is completely full."""
    return all(cell != " " for row in board for cell in row)

def check_for_win(board, player_checker):
    """Check board if player_checker has won (horizontal, vertical, diagonal)."""
    for row in range(ROWS):
        for col in range(COLS):
            # Only check from positions occupied by player_checker
            if board[row][col] != player_checker:
                continue
            # Horizontal
            if col <= COLS - 4 and all(board[row][col + offset] == player_checker for offset in range(4)):
                return True
            # Vertical
            if row <= ROWS - 4 and all(board[row + offset][col] == player_checker for offset in range(4)):
                return True
            # Diagonal down-right
            if row <= ROWS - 4 and col <= COLS - 4 and all(board[row + offset][col + offset] == player_checker for offset in range(4)):
                return True
            # Diagonal down-left
            if row <= ROWS - 4 and col >= 3 and all(board[row + offset][col - offset] == player_checker for offset in range(4)):
                return True
    return False

def next_player(current_index, num_players):
    """Returns the next player's index according to the number of players."""
    return (current_index + 1) % num_players

def main():
    # Use only the number of players and allowed checkers
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Create board
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Print board before the game starts
    clear_screen()
    print_board(board, COLS)

    while True:
        player_checker = players[current_player_idx]
        print()
        print(f"It's Player {player_checker}'s turn.")

        # Ask for a valid move
        col_index = get_player_input(player_checker, COLS)
        successful_move = drop_checker(board, col_index, player_checker)

        clear_screen()
        print_board(board, COLS)

        if not successful_move:
            print(f"Column {string.ascii_uppercase[col_index]} is full. Sorry, Player {player_checker} loses their turn!")
        else:
            # Check for a win
            if check_for_win(board, player_checker):
                print(f"Player {player_checker} won!")
                break
            # Check for a draw
            elif is_board_full(board):
                print("It's a draw!")
                break

        # Move to the next player (even if unsuccessful, turn is lost)
        current_player_idx = next_player(current_player_idx, NUM_PLAYERS)

if __name__ == "__main__":
    main()
