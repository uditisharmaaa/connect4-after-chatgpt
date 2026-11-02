import os
import random

# Constants for players
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Adjust this value based on the desired number of players (2 to 5)
PLAYERS = PLAYERS[:NUM_PLAYERS]

# Game constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Clear screen
def clear_screen():
    os.system('clear')  # Use 'cls' for Windows

# Display the board
def display_board(board):
    clear_screen()
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("| " + " | ".join(row) + " |")
    print("=" * (COLUMNS * 4 + 1))

# Check for a win
def check_win(board, player):
    # Check horizontal, vertical, and diagonal (both directions) for a win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == player for i in range(4)):
                return True

    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == player for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == player for i in range(4)) or all(board[row+i][col+3-i] == player for i in range(4)):
                return True
                
    return False

# Check for draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Get the next available row for a given column
def get_next_open_row(board, col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

# Main game function
def play_game():
    board = create_board()
    game_over = False
    turn = 0
    current_player = random.choice(PLAYERS)  # Choose a random starting player

    while not game_over:
        display_board(board)
        player = PLAYERS[turn % len(PLAYERS)]
        print(f"It's {player}'s turn.")

        # Validate input
        while True:
            col_input = input("Choose a column (A-G): ").strip().upper()
            if col_input in COLUMN_LABELS:
                col = COLUMN_LABELS.index(col_input)
                if board[0][col] == ' ':
                    break
            print("Invalid input. Please try again.")

        row = get_next_open_row(board, col)
        board[row][col] = player

        if check_win(board, player):
            display_board(board)
            print(f"Player {player} wins!")
            game_over = True
        elif check_draw(board):
            display_board(board)
            print("It's a draw!")
            game_over = True
        else:
            turn += 1

play_game()
