import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Allow 2 to 5 players
NUM_PLAYERS = 3  # You can change this between 2 to 5
assert 2 <= NUM_PLAYERS <= 5

# Initialize board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Display board
def display_board(board):
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    print(" +---+---+---+---+---+---+---+")
    for row in board:
        print(" | " + " | ".join(row) + " | ")
        print(" +---+---+---+---+---+---+---+")

# Check if a column is valid and open
def is_valid_move(board, column):
    return board[0][column] == ' '

# Place marker on board
def place_marker(board, column, marker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = marker
            return

# Check win conditions
def check_win(board, marker):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLUMNS):
            # Horizontal
            if c <= COLUMNS - 4 and all(board[r][c+i] == marker for i in range(4)):
                return True
            # Vertical
            if r <= ROWS - 4 and all(board[r+i][c] == marker for i in range(4)):
                return True
            # Diagonal right
            if r <= ROWS - 4 and c <= COLUMNS - 4 and all(board[r+i][c+i] == marker for i in range(4)):
                return True
            # Diagonal left
            if r <= ROWS - 4 and c >= 3 and all(board[r+i][c-i] == marker for i in range(4)):
                return True
    return False

# Check draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def connect_four():
    board = create_board()
    players = PLAYERS[:NUM_PLAYERS]
    random.shuffle(players)  # Randomize starting player
    turn_index = 0
    game_over = False

    while not game_over:
        current_player = players[turn_index]
        display_board(board)
        print(f"Player {current_player}'s turn. Choose a column (A-G):")

        # Input validation
        valid_input = False
        while not valid_input:
            choice = input().strip().upper()
            if choice in 'ABCDEFG':
                column = ord(choice) - ord('A')
                if is_valid_move(board, column):
                    valid_input = True
                else:
                    print("Column is full. Choose another column:")
            else:
                print("Invalid input. Please choose a column (A-G):")

        place_marker(board, column, current_player)

        if check_win(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            game_over = True
        elif check_draw(board):
            display_board(board)
            print("Game is a draw!")
            game_over = True

        turn_index = (turn_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    connect_four()
