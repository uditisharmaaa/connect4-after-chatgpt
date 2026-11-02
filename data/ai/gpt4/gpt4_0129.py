import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols for up to 5 players

# Board setup
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column labels
    print("  " + "   ".join([chr(65 + col) for col in range(COLUMNS)]))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Input validation
def get_valid_column(board, player):
    while True:
        column = input(f"Player {CHECKERS[player]}, please enter a column: ").strip().upper()
        if len(column) == 1 and 'A' <= column <= chr(65 + COLUMNS - 1):
            col_index = ord(column) - 65
            if board[0][col_index] == " ":
                return col_index
            else:
                print("Column is full. Choose a different column.")
        else:
            print("Invalid input. Enter a valid column letter.")

# Drop checker in selected column
def drop_checker(board, col_index, player):
    for row in reversed(range(ROWS)):
        if board[row][col_index] == " ":
            board[row][col_index] = CHECKERS[player]
            return row

# Win check
def check_winner(board, player, row, col):
    def count_checkers(delta_row, delta_col):
        count = 0
        r, c = row + delta_row, col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == CHECKERS[player]:
            count += 1
            r += delta_row
            c += delta_col
        return count

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1  # Count the current checker
        count += count_checkers(dr, dc)  # Check forward direction
        count += count_checkers(-dr, -dc)  # Check backward direction
        if count >= 4:
            return True
    return False

# Draw check
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main game loop
def connect_4():
    board = create_board()
    players = PLAYERS

    # Randomly select first player
    current_player = random.randint(0, players - 1)

    print_board(board)

    while True:
        # Get valid column and drop checker
        col_index = get_valid_column(board, current_player)
        row_index = drop_checker(board, col_index, current_player)
        
        print_board(board)

        # Check for win
        if check_winner(board, current_player, row_index, col_index):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % players

if __name__ == "__main__":
    connect_4()
