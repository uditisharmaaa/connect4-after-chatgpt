import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Symbols for up to 5 players

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def initialize_board():
    """Create and return an empty board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    clear_screen()
    print("  " + " ".join(list("ABCDEFG")))
    for row in board:
        print("|" + "|".join(row) + "|")
    print(" " + "-" * (COLUMNS * 2 - 1))

def is_valid_move(board, column):
    """Check if a move is valid (i.e., column is not full)."""
    return board[0][column] == ' '

def make_move(board, column, symbol):
    """Place the player's symbol in the chosen column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = symbol
            return

def check_winner(board, symbol):
    """Check if the given symbol has a winning line."""
    # Check horizontal, vertical, and diagonal lines for a win
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (
                col <= COLUMNS - 4 and all(board[row][col + i] == symbol for i in range(4)) or
                row <= ROWS - 4 and all(board[row + i][col] == symbol for i in range(4)) or
                row <= ROWS - 4 and col <= COLUMNS - 4 and all(board[row + i][col + i] == symbol for i in range(4)) or
                row <= ROWS - 4 and col >= 3 and all(board[row + i][col - i] == symbol for i in range(4))
            ):
                return True
    return False

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def get_player_move(player_symbols, current_player):
    """Get the move from the current player."""
    column_input = input(f"Player {player_symbols[current_player]}'s turn. Enter column (A-G): ").upper()
    if column_input in "ABCDEFG" and len(column_input) == 1:
        return ord(column_input) - ord('A')
    else:
        return None

def play_game(player_count):
    """Main game logic."""
    board = initialize_board()
    current_player = random.randint(0, player_count - 1)
    while True:
        print_board(board)
        
        # Get and validate player move
        column = get_player_move(PLAYER_SYMBOLS, current_player)
        if column is None or not is_valid_move(board, column):
            print("Invalid move. Please try again.")
            continue
        
        # Make the move
        make_move(board, column, PLAYER_SYMBOLS[current_player])
        
        # Check for a win or draw
        if check_winner(board, PLAYER_SYMBOLS[current_player]):
            print_board(board)
            print(f"Player {PLAYER_SYMBOLS[current_player]} wins!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % player_count

def main():
    player_count = 5  # Set the number of players from 2 to 5
    if 2 <= player_count <= 5:
        play_game(player_count)
    else:
        print("Invalid number of players. Please set a player count between 2 and 5.")

if __name__ == "__main__":
    main()
