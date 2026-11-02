import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # A, B, C...

# Initialize the board
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear screen
    print("  " + "   ".join(COLUMN_LABELS[:len(board[0])]))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check for a win
def check_win(board, player_checker):
    for r in range(ROWS):
        for c in range(COLUMNS):
            # Check horizontal
            if c + 3 < COLUMNS and all(board[r][c + i] == player_checker for i in range(4)):
                return True
            # Check vertical
            if r + 3 < ROWS and all(board[r + i][c] == player_checker for i in range(4)):
                return True
            # Check diagonal (bottom-right)
            if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == player_checker for i in range(4)):
                return True
            # Check diagonal (top-right)
            if r - 3 >= 0 and c + 3 < COLUMNS and all(board[r - i][c + i] == player_checker for i in range(4)):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

# Drop a checker into the board
def drop_checker(board, column, player_checker):
    for r in reversed(range(ROWS)):
        if board[r][column] == ' ':
            board[r][column] = player_checker
            return True
    return False

# Get valid column from the player
def get_valid_column(board):
    while True:
        col = input("Please enter a column: ").upper()
        if col not in COLUMN_LABELS[:COLUMNS]:
            print("Invalid column. Try again.")
            continue
        col_index = COLUMN_LABELS.index(col)
        if board[0][col_index] != ' ':
            print("Column is full. Try again.")
            continue
        return col_index

# Main function
def play_game():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)
    print(f"Randomly selected Player {players[current_player]} to start.")

    while True:
        print(f"Player {players[current_player]}'s turn.")
        column = get_valid_column(board)

        drop_checker(board, column, players[current_player])
        print_board(board)

        if check_win(board, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
