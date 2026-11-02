import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CONNECT_NUM = 4

# Create the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clears the console
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Place checker in the column
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

# Check for a win condition
def check_win(board, checker):
    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(CONNECT_NUM)):
                return True

    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == checker for i in range(CONNECT_NUM)):
                return True

    # Check diagonal (positive slope)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == checker for i in range(CONNECT_NUM)):
                return True

    # Check diagonal (negative slope)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == checker for i in range(CONNECT_NUM)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

# Get player input and validate
def get_valid_move(player_checker):
    while True:
        move = input(f"Player {player_checker}, please enter a column: ")
        if len(move) != 1 or not move.isalpha() or not ("A" <= move <= chr(65 + COLUMNS - 1)):
            print("Invalid input, please enter a valid column letter.")
            continue
        column = ord(move.upper()) - ord('A')
        if board[0][column] != " ":
            print("Column full, choose another column.")
            continue
        return column

# Main game loop
def play_game():
    # Initialize board and players
    board = create_board()
    players = ["X", "O", "V", "H", "M"]
    num_players = 2  # For submission, use 2 players
    player_checkers = players[:num_players]

    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    current_player = player_checkers[current_player_index]

    # Print initial game state
    print_board(board)

    while True:
        column = get_valid_move(current_player)
        place_checker(board, column, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players
        current_player = player_checkers[current_player_index]

# Run the game
if __name__ == "__main__":
    play_game()
