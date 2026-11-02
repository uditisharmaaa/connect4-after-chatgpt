import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to create empty board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Function to check if move is valid
def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == " "

# Function to drop a checker into the board
def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col

# Function to check for a win
def is_winner(board, last_row, last_col):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Vertical, Horizontal, Diagonal (/ and \)

    def count_checkers(delta_row, delta_col):
        count = 0
        r, c = last_row + delta_row, last_col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == board[last_row][last_col]:
            count += 1
            r += delta_row
            c += delta_col
        return count

    for dr, dc in directions:
        if count_checkers(dr, dc) + count_checkers(-dr, -dc) >= 3:  # Total >= 4 (including the last checker)
            return True
    return False

# Function to check for a draw
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game function
def play_connect4():
    # Initial setup
    board = create_board()
    num_players = 2  # Default to 2 players
    players = [CHECKERS[i] for i in range(num_players)]
    current_player = random.randint(0, num_players - 1)  # Randomly select first player

    print_board(board)
    print(f"Player {players[current_player]}'s turn!")

    while True:
        # Get player input
        col = -1
        while True:
            try:
                move = input(f"Player {players[current_player]}, please enter a column: ")
                if len(move) != 1 or not move.isalpha():
                    raise ValueError
                col = ord(move.upper()) - ord('A')
                if not is_valid_move(board, col):
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter a valid column letter (A-G).")

        # Place the checker
        row, col = drop_checker(board, col, players[current_player])
        print_board(board)

        # Check for win
        if is_winner(board, row, col):
            print(f"Player {players[current_player]} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % num_players

# Run the game
if __name__ == "__main__":
    play_connect4()
