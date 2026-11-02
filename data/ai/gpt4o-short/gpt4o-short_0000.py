import random
import os

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Settings
PLAYERS_COUNT = 3  # Change this number to set how many players play (2 to 5)

# Initialize board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the screen
    print("Current board:")
    print(" | ".join(COLUMN_LABELS))
    print("-" * (COLUMNS * 4 - 1))
    for row in board:
        print(" | ".join(row))
    print()

def check_valid_move(board, column):
    return board[0][column] == ' '

def make_move(board, column, symbol):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = symbol
            break

def check_winner(board, symbol):
    # Check horizontal
    for row in board:
        for c in range(COLUMNS - 3):
            if row[c] == row[c + 1] == row[c + 2] == row[c + 3] == symbol:
                return True

    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] == symbol:
                return True

    # Check diagonal (positive slope)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] == symbol:
                return True

    # Check diagonal (negative slope)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3] == symbol:
                return True

    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def play_game():
    board = create_board()
    players = PLAYER_SYMBOLS[:PLAYERS_COUNT]
    current_player_index = random.randint(0, PLAYERS_COUNT - 1)

    while True:
        print_board(board)
        current_player = players[current_player_index]
        move_valid = False
        while not move_valid:
            move = input(f"Player {current_player}, choose a column (A-G): ").upper()
            if move in COLUMN_LABELS:
                column = COLUMN_LABELS.index(move)
                if check_valid_move(board, column):
                    make_move(board, column, current_player)
                    move_valid = True
                else:
                    print("Column full! Choose a different column.")
            else:
                print("Invalid input! Please enter a valid column (A-G).")

        # Check for win or draw
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Move to the next player
        current_player_index = (current_player_index + 1) % PLAYERS_COUNT

# Run the game
if __name__ == "__main__":
    play_game()
