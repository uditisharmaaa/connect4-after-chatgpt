import os
import random

# Constants for the game
ROWS = 6
COLS = 7
COLUMNS_MAPPING = 'ABCDEFG'
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Set this to between 2 and 5
EMPTY_SLOT = '.'

def create_board():
    board = [[EMPTY_SLOT for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    os.system('clear')

    print("  ".join(COLUMNS_MAPPING))
    for row in board:
        print(" | ".join(row))
        print("-" * (COLS * 4 - 1))

def is_valid_column(board, col):
    return board[0][col] == EMPTY_SLOT

def get_next_open_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY_SLOT:
            return row
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

    return False

def is_draw(board):
    for c in range(COLS):
        if is_valid_column(board, c):
            return False
    return True

def main():
    board = create_board()
    print_board(board)

    # Begin game loop
    game_over = False
    players = PLAYER_TOKENS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while not game_over:
        try:
            # Get input from player
            col_input = input(f"Player {current_player}, make your move (A-{COLUMNS_MAPPING[COLS-1]}): ").strip().upper()
            
            if col_input not in COLUMNS_MAPPING[:COLS]:
                raise ValueError("Invalid column")

            col = COLUMNS_MAPPING.index(col_input)

            if not is_valid_column(board, col):
                print("Column is full. Choose another column.")
                continue

            row = get_next_open_row(board, col)
            drop_piece(board, row, col, current_player)

            if winning_move(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                game_over = True
            elif is_draw(board):
                print_board(board)
                print("The game is a draw!")
                game_over = True
            else:
                # Switch to next player
                current_player_index = players.index(current_player)
                current_player = players[(current_player_index + 1) % len(players)]

            print_board(board)

        except ValueError as ve:
            print(ve)
            continue

if __name__ == "__main__":
    main()
