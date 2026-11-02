import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Adjust this to 2-5 players
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Display the board
def print_board(board):
    os.system('clear')  # Unix/Linux/Mac
    print(" ".join(COLUMN_LABELS))
    for row in board:
        print("|".join(row))
        print("-" * (2 * COLUMNS - 1))

# Check if a move is valid
def is_valid_move(board, column):
    return board[0][column] == ' '

# Get the first available row in the selected column
def get_next_open_row(board, column):
    for r in range(ROWS-1, -1, -1):
        if board[r][column] == ' ':
            return r
    return None  # Shouldn't reach here with proper move validation

# Place the piece in the board
def drop_piece(board, row, column, piece):
    board[row][column] = piece

# Check for a win
def check_win(board, piece):
    # Check horizontal locations
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

# Main game logic
def connect_4():
    board = create_board()
    num_players = len(PLAYER_SYMBOLS)
    current_player_index = random.randint(0, num_players - 1)
    game_over = False

    print_board(board)

    while not game_over:
        current_player = PLAYER_SYMBOLS[current_player_index]
        print(f"Player {current_player}'s turn")

        # Input and validation
        valid_move = False
        while not valid_move:
            column_selection = input(f"Player {current_player}, select a column (A-G): ").upper()
            if column_selection in COLUMN_LABELS:
                column = COLUMN_LABELS.index(column_selection)
                if is_valid_move(board, column):
                    valid_move = True
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid column, please choose a column from A to G.")

        # Drop the piece
        row = get_next_open_row(board, column)
        drop_piece(board, row, column, current_player)

        # Print the board
        print_board(board)

        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} wins!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to the next player
            current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    connect_4()
