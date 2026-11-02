import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for up to 5 players
NUM_PLAYERS = 2  # Number of active players (default 2)

# Function to clear screen
def clear_screen():
    os.system('clear')

# Function to initialize the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    col_labels = " " + "   ".join(chr(65 + i) for i in range(COLS))
    print(col_labels)
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Function to validate input and return column index
def get_valid_column():
    while True:
        user_input = input("Enter a column: ").upper()
        if len(user_input) == 1 and "A" <= user_input <= chr(65 + COLS - 1):
            col = ord(user_input) - 65
            if board[0][col] == " ":
                return col
            else:
                print("Column is full. Try again.")
        else:
            print("Invalid input. Try again.")

# Function to drop checker in a column
def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col

# Function to check for a win
def check_win(board, checker, row, col):
    def count_checkers(dx, dy):
        count = 0
        x, y = row + dx, col + dy
        while 0 <= x < ROWS and 0 <= y < COLS and board[x][y] == checker:
            count += 1
            x, y = x + dx, y + dy
        return count

    # Check horizontally, vertically, diagonally (both directions)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        if 1 + count_checkers(dx, dy) + count_checkers(-dx, -dy) >= 4:
            return True
    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game logic
if __name__ == "__main__":
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)
    print(f"Player {CHECKERS[current_player]} starts!")

    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}'s turn.")
        col = get_valid_column()

        # Drop the checker
        row, col = drop_checker(board, col, CHECKERS[current_player])

        # Check for win
        if check_win(board, CHECKERS[current_player], row, col):
            clear_screen()
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS
        clear_screen()
