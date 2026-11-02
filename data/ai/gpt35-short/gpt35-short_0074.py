import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = ['A','B','C','D','E','F','G']

# Possible player pieces
PLAYER_PIECES = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    # Clear terminal screen (works in Unix-based systems)
    os.system('clear')

def create_board():
    # Create empty board represented by a 2D list filled with spaces
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print(' ' + ' '.join(COL_LABELS))
    # Print each row
    for row in board:
        print('|' + '|'.join(row) + '|')
    # Print bottom border
    print(' ' + '-'.join(['-' for _ in range(COLS)]))

def is_valid_column(col_idx, board):
    # Column is valid if top cell is empty (means we can drop piece there)
    return 0 <= col_idx < COLS and board[0][col_idx] == ' '

def get_next_open_row(col_idx, board):
    # Return the lowest empty row in the column, or -1 if none
    for r in range(ROWS-1, -1, -1):
        if board[r][col_idx] == ' ':
            return r
    return -1

def drop_piece(board, row, col, piece):
    # Place the piece in the board at the specified row and column
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal locations for win
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Check positively sloped diagonals (\)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals (/)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def is_board_full(board):
    # If no empty spaces on top row, board is full
    return all(cell != ' ' for cell in board[0])

def get_num_players():
    # Prompt for number of players between 2 and 5
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer between 2 and 5.")

def get_player_move(player_piece):
    # Ask the current player to select a column A-G
    while True:
        move = input(f"Player {player_piece}, choose a column (A-G): ").upper()
        if move in COL_LABELS:
            return COL_LABELS.index(move)
        else:
            print("Invalid input. Please enter a letter A-G corresponding to a column.")

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_num_players()
    players = PLAYER_PIECES[:num_players]

    # Randomly select first player index
    current_player_idx = random.randint(0, num_players - 1)

    board = create_board()
    game_over = False

    while not game_over:
        clear_screen()
        print_board(board)
        current_piece = players[current_player_idx]

        # Get valid column from player
        col = get_player_move(current_piece)

        # Check if the chosen column is not full
        if not is_valid_column(col, board):
            print(f"Column {COL_LABELS[col]} is full. Choose another column.")
            input("Press Enter to continue...")
            continue

        # Find next open row in the chosen column
        row = get_next_open_row(col, board)
        drop_piece(board, row, col, current_piece)

        # Check for win
        if winning_move(board, current_piece):
            clear_screen()
            print_board(board)
            print(f"Player {current_piece} wins! Congratulations!")
            game_over = True
            continue

        # Check for draw
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw! No more moves possible.")
            game_over = True
            continue

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % num_players

    print("Game over. Thanks for playing!")

if __name__ == "__main__":
    main()
