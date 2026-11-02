import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(65 + i) for i in range(COLUMNS)]  # 'A', 'B', 'C', ...

# Initialize the game board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the console
    print("  " + "   ".join(COLUMN_LABELS[:len(board[0])]))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

# Get the lowest available row in a column
def get_row(board, column):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            return row
    return None  # Column is full

# Check for a win
def check_winner(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (/)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main game loop
def play_game():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {players[current_player_index]}, it's your turn.")
        column = None

        # Get valid input
        while True:
            try:
                user_input = input("Please enter a column: ").strip().upper()
                if user_input not in COLUMN_LABELS[:COLUMNS]:
                    raise ValueError("Invalid column label.")
                column = COLUMN_LABELS.index(user_input)
                if get_row(board, column) is None:
                    print("Column is full. Try again.")
                    continue
                break
            except ValueError as e:
                print(e)

        row = get_row(board, column)
        board[row][column] = players[current_player_index]
        print_board(board)

        # Check for win or draw
        if check_winner(board, players[current_player_index]):
            print(f"Player {players[current_player_index]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch player
        current_player_index = (current_player_index + 1) % PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
