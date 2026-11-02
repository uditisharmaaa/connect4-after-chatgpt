import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
COLUMN_LABELS = [chr(65 + i) for i in range(COLUMNS)]  # ['A', 'B', 'C', ..., 'G']

# Function to create the game board
def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

# Function to print the game board
def print_board(board):
    os.system('clear')  # Clear terminal screen
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + ('---+' * COLUMNS))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + ('---+' * COLUMNS))
    print()

# Function to check if the input column is valid
def is_valid_column(column, board):
    return column in COLUMN_LABELS and board[0][COLUMN_LABELS.index(column)] == ' '

# Function to place the checker in the chosen column
def place_checker(board, column, symbol):
    col_index = COLUMN_LABELS.index(column)
    for row_index in range(ROWS - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == ' ':
            board[row_index][col_index] = symbol
            return row_index, col_index

# Function to check for a win condition
def check_for_win(board, row, col, symbol):
    def check_direction(delta_row, delta_col):
        count = 1
        for direction in (1, -1):  # Check both directions
            r, c = row, col
            while True:
                r += delta_row * direction
                c += delta_col * direction
                if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == symbol:
                    count += 1
                else:
                    break
        return count

    # Check horizontal, vertical, diagonal down-right, diagonal down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        if check_direction(dr, dc) >= 4:
            return True
    return False

# Function to check if the board is full (draw condition)
def check_for_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game function
def connect_4():
    # Initialize board and players
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_SYMBOLS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    # Main game loop
    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column: ", end='')

        column = input().strip().upper()

        if is_valid_column(column, board):
            row, col = place_checker(board, column, current_player)
            print_board(board)

            # Check win condition
            if check_for_win(board, row, col, current_player):
                print(f"Player {current_player} won!")
                break

            # Check draw condition
            if check_for_draw(board):
                print("The game is a draw!")
                break

            # Switch to next player
            current_player_index = (current_player_index + 1) % PLAYERS
        else:
            print("Invalid input. Please try again.")

# Run the game
if __name__ == "__main__":
    connect_4()
