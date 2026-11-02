import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2  # Set the number of players (between 2 and 5)

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the console
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (2 * COLS + 1))

def is_valid_move(board, col):
    return board[0][col] == ' '

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def check_for_win(board, piece):
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    # Create board
    board = create_board()
    print_board(board)

    # Randomly select first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Game loop
    game_over = False
    while not game_over:
        player_piece = PLAYERS[current_player_idx]
        move = input(f"Player {player_piece}, make your move (A-G): ").strip().upper()
        
        if move not in COLUMN_LABELS:
            print("Invalid column. Choose between A-G.")
            continue

        col = COLUMN_LABELS.index(move)

        if is_valid_move(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, player_piece)
            print_board(board)

            if check_for_win(board, player_piece):
                print(f"Player {player_piece} wins!")
                game_over = True
            elif is_draw(board):
                print("The game is a draw!")
                game_over = True
            else:
                current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        else:
            print("Column full, try another move.")

if __name__ == "__main__":
    main()
