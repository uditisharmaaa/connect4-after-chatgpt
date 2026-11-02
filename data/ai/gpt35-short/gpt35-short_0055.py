import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_PIECES = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + " ".join(COL_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def is_valid_column(board, col_index):
    # Check if the top row in the column is empty (meaning you can drop a piece)
    return board[0][col_index] == ' '

def get_next_open_row(board, col_index):
    for r in range(ROWS-1, -1, -1):
        if board[r][col_index] == ' ':
            return r
    return None  # Should not happen if is_valid_column returns True

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def check_win(board, piece):
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

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def is_draw(board):
    # If no spaces in top row, board is full
    return all(space != ' ' for space in board[0])

def get_player_count():
    while True:
        try:
            count = int(input(f"Enter number of players (2 to 5): "))
            if 2 <= count <= 5:
                return count
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_player_move(player_piece):
    while True:
        move = input(f"Player {player_piece}, choose a column (A-G): ").upper()
        if len(move) == 1 and move in COL_LABELS:
            return COL_LABELS.index(move)
        else:
            print("Invalid column. Please choose a letter from A to G.")

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_player_count()
    players = PLAYER_PIECES[:num_players]

    board = create_board()
    current_player_idx = random.randint(0, num_players - 1)
    
    while True:
        clear_screen()
        print_board(board)
        current_piece = players[current_player_idx]
        
        # Get valid column input
        while True:
            col = get_player_move(current_piece)
            if is_valid_column(board, col):
                break
            else:
                print(f"Column {COL_LABELS[col]} is full. Choose another.")

        row = get_next_open_row(board, col)
        drop_piece(board, row, col, current_piece)

        # Check for win
        if check_win(board, current_piece):
            clear_screen()
            print_board(board)
            print(f"Player {current_piece} wins! Congratulations!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
