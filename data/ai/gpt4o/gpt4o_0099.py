import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
WIN_LENGTH = 4
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Use 'cls' instead of 'clear' on Windows
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check for valid input
def is_valid_input(input_str):
    return len(input_str) == 1 and 'A' <= input_str <= chr(ord('A') + COLUMNS - 1)

# Check if the move is allowed
def is_move_allowed(board, col):
    return board[0][col] == ' '

# Place the checker
def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            break

# Check for a win
def check_for_win(board, checker):
    # Check horizontal, vertical and diagonal
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == checker:
                if col <= COLUMNS - WIN_LENGTH and all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                    return True
                if row <= ROWS - WIN_LENGTH and all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                    return True
                if row <= ROWS - WIN_LENGTH and col <= COLUMNS - WIN_LENGTH and all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                    return True
                if row <= ROWS - WIN_LENGTH and col >= WIN_LENGTH - 1 and all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                    return True
    return False

# Check for a draw
def check_for_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Main game loop
def connect_four(players_count=2):
    board = create_board()
    player_symbols = PLAYER_SYMBOLS[:players_count]
    current_player = random.choice(player_symbols)
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip().upper()

        if not is_valid_input(user_input):
            print("Invalid input, please enter a letter of the column.")
            continue

        col = ord(user_input) - ord('A')
        if not is_move_allowed(board, col):
            print("Column full, turn lost. Next player's turn.")
            current_player = player_symbols[(player_symbols.index(current_player) + 1) % players_count]
            continue

        place_checker(board, col, current_player)
        print_board(board)

        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_for_draw(board):
            print("The game is a draw!")
            break

        current_player = player_symbols[(player_symbols.index(current_player) + 1) % players_count]

# Run the game
if __name__ == "__main__":
    connect_four(players_count=2)
