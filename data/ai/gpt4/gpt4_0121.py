import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

# Helper function to create an empty board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Helper function to print the board
def print_board(board):
    os.system('clear')  
    column_labels = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Helper function to check if a move is valid
def is_valid_move(board, column):
    col_idx = ord(column) - ord('A')
    return 0 <= col_idx < len(board[0]) and board[0][col_idx] == " "

# Helper function to drop a checker in the column
def drop_checker(board, column, checker):
    col_idx = ord(column) - ord('A')
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = checker
            break

# Helper function to check if a player has won
def check_winner(board, checker):
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (up-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

# Helper function to check if board is full (draw)
def is_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game function
def play_game():
    # Initialize the game
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Default to 2 players
    current_players = PLAYERS[:num_players]
    current_player_idx = random.randint(0, num_players - 1)

    print_board(board)
    print(f"Player {current_players[current_player_idx]} starts!")

    # Game loop
    while True:
        current_player = current_players[current_player_idx]
        print_board(board)
        move = input(f"Player {current_player}, please enter a column: ").strip().upper()

        # Validate move
        if len(move) == 1 and move.isalpha() and is_valid_move(board, move):
            drop_checker(board, move, current_player)
            # Check for winner
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            # Check for draw
            if is_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            # Switch to next player
            current_player_idx = (current_player_idx + 1) % num_players
        else:
            print("Invalid move. Try again.")
            continue

# Run the game
if __name__ == "__main__":
    play_game()
