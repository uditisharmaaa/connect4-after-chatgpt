import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = "ABCDEFG"
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:5]  # Maximum 5 players, fewer players will adjust dynamically

# Function to clear the terminal
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def display_board(board):
    """Display the current game board."""
    clear_screen()
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print(" " + "-" * (2 * COLUMNS - 1))

def get_random_player():
    """Pick a random player to start."""
    return random.choice(PLAYERS)

def get_player_move(current_player, board):
    """Prompt the player for a move and validate it."""
    while True:
        move = input(f"Player {current_player}, choose a column ({COLUMN_LABELS}): ").strip().upper()
        if move in COLUMN_LABELS:
            column_index = COLUMN_LABELS.index(move)
            if board[0][column_index] == ' ':  # Check if the column is not full
                return column_index
            else:
                print("That column is full! Choose a different one.")
        else:
            print(f"Invalid input! Please choose a column ({COLUMN_LABELS}).")

def drop_piece(board, column, player):
    """Drop a piece into the chosen column for the player."""
    for row in reversed(board):  # Start from the bottom row
        if row[column] == ' ':
            row[column] = player
            break

def is_winner(board, player):
    """Check if the player has won the game."""
    # Check horizontal, vertical, and diagonal conditions
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (col + 3 < COLUMNS and all(board[row][col + i] == player for i in range(4))) or \
               (row + 3 < ROWS and all(board[row + i][col] == player for i in range(4))) or \
               (col + 3 < COLUMNS and row + 3 < ROWS and all(board[row + i][col + i] == player for i in range(4))) or \
               (col - 3 >= 0 and row + 3 < ROWS and all(board[row + i][col - i] == player for i in range(4))):
                return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game loop."""
    # Initialize the game
    board = create_board()
    num_players = len(PLAYERS)  # Set the number of players from the constant list
    current_player_index = PLAYERS.index(get_random_player())
    display_board(board)
    
    while True:
        current_player = PLAYERS[current_player_index]
        column = get_player_move(current_player, board)
        drop_piece(board, column, current_player)
        display_board(board)
        
        if is_winner(board, current_player):
            print(f"Player {current_player} wins!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
