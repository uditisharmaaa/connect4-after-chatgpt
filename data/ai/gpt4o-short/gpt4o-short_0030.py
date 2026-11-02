import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Change this to a value between 2 and 5 as needed
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']
selected_players = PLAYER_MARKERS[:PLAYERS]

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Use 'clear' on Unix/Linux/MacOS, use 'cls' on Windows
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("| " + " | ".join(row) + " |")
    print("-" * 29)

# Check for a win
def check_win(board, marker):
    # Check horizontal, vertical, and diagonal combinations for a win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == marker for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == marker for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == marker for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == marker for i in range(4)):
                return True
    return False

# Check for draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Get the next available row in the column
def get_next_open_row(board, col):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            return row
    return None

# Main game function
def play_game():
    board = create_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    game_over = False
    alphabet = 'ABCDEFG'
    
    while not game_over:
        print_board(board)
        player = selected_players[current_player_index]
        move = input(f"Player {player}, choose a column (A-G): ").strip().upper()

        if move not in alphabet:
            print("Invalid input. Please enter a letter from A to G.")
            continue
        
        col = alphabet.index(move)
        row = get_next_open_row(board, col)
        
        if row is None:
            print("Column is full. Please choose another column.")
            continue

        board[row][col] = player

        if check_win(board, player):
            print_board(board)
            print(f"Player {player} wins!")
            game_over = True

        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
