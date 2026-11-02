import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Used based on number of players
MIN_PLAYERS = 2  # Minimum players required

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board():
    """Initialize a blank board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_column(column):
    """Check if the column is within bounds."""
    return 0 <= column < COLS

def is_column_full(board, column):
    """Check if the column is full."""
    return board[0][column] != ' '  # Top row is occupied

def drop_checker(board, column, checker):
    """Place the checker in the lowest unoccupied space in the column."""
    for row in range(ROWS - 1, -1, -1):  # Start from bottom
        if board[row][column] == ' ':
            board[row][column] = checker
            return row, column

def is_winner(board, row, col, checker):
    """Check if the current move resulted in a win."""
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Down, Right, Diagonal right down, Diagonal left down

    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False

def is_draw(board):
    """Check if the board is completely filled and it's a draw."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main game function."""
    # Setup
    board = create_board()
    player_count = 2  # Set to MIN_PLAYERS for this submission
    active_players = PLAYERS[:player_count]
    current_player_index = random.randint(0, player_count - 1)
    winner = None

    # Game loop
    while not winner:
        print_board(board)
        current_player = active_players[current_player_index]
        print(f"Player {current_player}, it's your turn.")

        while True:
            column_input = input("Please enter a column: ").strip().upper()

            if len(column_input) == 1 and 'A' <= column_input <= chr(64 + COLS):
                column = ord(column_input) - 65  # Convert letter to column index
                if is_valid_column(column):
                    if not is_column_full(board, column):
                        break
                    else:
                        print(f"Column {column_input} is full. Try a different column.")
                else:
                    print(f"Invalid column {column_input}. Please try again.")
            else:
                print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")

        # Place the checker and check for a win or draw
        row, col = drop_checker(board, column, current_player)

        if is_winner(board, row, col, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            winner = current_player
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % player_count

if __name__ == "__main__":
    play_game()
