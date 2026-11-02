import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+---" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row contents
        print("+---" + "---+" * COLS)  # Row separator

# Get valid input from user
def get_valid_input(player, board):
    while True:
        column = input(f"Player {player}, please enter a column (A-G): ").upper()
        if column in (chr(65 + i) for i in range(COLS)):
            col_index = ord(column) - 65
            if board[0][col_index] == ' ':
                return col_index
            else:
                print("Column is full, try another column.")
        else:
            print("Invalid input, please try again.")

# Place the checker in the specified column
def place_checker(board, col_index, checker):
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return True
    return False

# Check for a win in different directions
def check_win(board, checker):
    # Check horizontal, vertical, and diagonal directions
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                if (c + 3 < COLS and all(board[r][c + i] == checker for i in range(4))) or \
                   (r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4))) or \
                   (r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4))) or \
                   (r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == checker for i in range(4))):
                    return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Main game function
def connect_4():
    board = create_board()
    num_players = min(MAX_PLAYERS, 2)  # Configured to 2 players
    players = PLAYERS[:num_players]

    current_player = random.choice(players)
    print_board(board)

    while True:
        col_index = get_valid_input(current_player, board)
        place_checker(board, col_index, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player = players[(players.index(current_player) + 1) % num_players]

# Start the game
if __name__ == "__main__":
    connect_4()
