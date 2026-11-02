import random
import os

# Constants for game configuration
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Maximum of 5 players

# Function to initialize the game board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear' if os.name == 'posix' else 'cls')
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("=" * (2 * COLUMNS + 1))

# Function to check if a column is valid for a move
def is_valid_move(board, col):
    return board[0][col] == ' '

# Function to make a move for a player
def make_move(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            break

# Function to check win condition
def check_win(board, player):
    # Check horizontal, vertical, and diagonal conditions for a win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

# Function to check if the board is full
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Main game loop
def play_game(num_players):
    board = create_board()
    current_player_index = random.randint(0, num_players - 1)
    players = PLAYERS[:num_players]

    while True:
        print_board(board)
        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn")

        # Get player input
        valid_input = False
        while not valid_input:
            move = input(f"Enter column (A-{COLUMN_LABELS[COLUMNS - 1]}): ").strip().upper()
            if move in COLUMN_LABELS:
                col = COLUMN_LABELS.index(move)
                if is_valid_move(board, col):
                    valid_input = True
                else:
                    print("Column full. Choose another.")
            else:
                print("Invalid input. Choose a valid column.")

        # Make move
        make_move(board, col, current_player)

        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    # Set number of players between 2 and 5
    num_players = 3  # You can change this value to test different number of players
    play_game(num_players)
