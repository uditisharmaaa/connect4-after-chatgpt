import random
import os

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYER_MARKS = ['X', 'O', 'V', 'H', 'M']  # Player markers, corresponding to the number of players
PLAYER_COUNT = 3  # Change this to set between 2 to 5 players

# Function to create the game board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    # Clear the terminal screen
    os.system('clear')
    # Print column headers
    print('  ' + ' '.join([chr(65 + i) for i in range(COLUMNS)]))
    # Print board's current state
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+' + '---' * COLUMNS + '+\n')

# Function to check if a column can accept another piece
def is_valid_column(board, column):
    return board[0][column] == ' '

# Get the next open row in the selected column
def get_next_open_row(board, column):
    for r in range(ROWS-1, -1, -1):
        if board[r][column] == ' ':
            return r
    return None

# Function to drop a piece into the board
def drop_piece(board, row, column, piece):
    board[row][column] = piece

# Check for win (horizontal, vertical, or diagonal)
def check_winner(board, piece):
    # Check horizontal locations for win
    for r in range(ROWS):
        for c in range(COLUMNS-3):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

# Check for draw
def check_draw(board):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == ' ':
                return False
    return True

# Main game loop
def play_game():
    board = create_board()
    game_over = False
    turn = random.randint(0, PLAYER_COUNT - 1)  # Randomly select who starts

    while not game_over:
        print_board(board)
        print(f"Player {PLAYER_MARKS[turn]}'s turn.")
        col_selected = input("Select a column (A-G): ").upper()

        if col_selected.isalpha() and 'A' <= col_selected <= 'G':
            col = ord(col_selected) - ord('A')

            if is_valid_column(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_MARKS[turn])

                if check_winner(board, PLAYER_MARKS[turn]):
                    print_board(board)
                    print(f"Player {PLAYER_MARKS[turn]} wins! Congratulations!")
                    game_over = True
                elif check_draw(board):
                    print_board(board)
                    print("The game is a draw!")
                    game_over = True
                else:
                    turn += 1
                    turn %= PLAYER_COUNT  # Go to next player
            else:
                print("Column is full, please choose another one.")
        else:
            print("Invalid input, please enter a letter between A-G.")

if __name__ == "__main__":
    play_game()
