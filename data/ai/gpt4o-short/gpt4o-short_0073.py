import random
import os

# Constants for game settings.
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Possible players
NUM_PLAYERS = 4  # Set up the number of players in this game

# Function to initialize the game board.
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the current state of the board.
def print_board(board):
    os.system('clear')  # Clears the terminal screen
    print("  A B C D E F G")
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLUMNS * 2 + 1))

# Function to check if a move is valid.
def is_valid_move(board, column):
    return board[0][column] == ' '

# Function to apply a move to the board.
def make_move(board, column, player):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return

# Function to check for a win condition.
def check_winner(board, player):
    # Check horizontal locations for a win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check vertical locations for a win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

# Function to check if the board is full (draw condition).
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Main function to manage the game state.
def play_game():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)  # Pick a random first player

    game_over = False

    while not game_over:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        move_valid = False

        while not move_valid:
            move = input(f"Player {current_player}, choose a column (A-G): ").upper()
            if move in "ABCDEFG" and len(move) == 1:
                column = ord(move) - ord('A')
                if is_valid_move(board, column):
                    make_move(board, column, current_player)
                    move_valid = True
                else:
                    print("That column is full. Choose a different one.")
            else:
                print("Invalid input. Please enter a letter from A to G.")

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True

        # Advance to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
play_game()
