import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Change this list to alter the number and types of players
NUM_PLAYERS = 2  # Change this number for more than two players (up to 5)
EMPTY_SLOT = '.'

def create_board():
    return [[EMPTY_SLOT for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print(' '.join(COLUMN_LABELS))
    for row in board:
        print(' '.join(row))
    print("\n")

def is_valid_column(board, col):
    return board[0][col] == EMPTY_SLOT

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == EMPTY_SLOT:
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal locations for a win
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for a win
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

def is_draw(board):
    return all(board[0][c] != EMPTY_SLOT for c in range(COLUMNS))

def get_player_choice():
    while True:
        choice = input("Enter a column (A-G): ").upper()
        if choice in COLUMN_LABELS:
            return COLUMN_LABELS.index(choice)
        print("Invalid input. Please choose a column between A and G.")

def main():
    board = create_board()
    print_board(board)
    
    current_player_index = random.randint(0, NUM_PLAYERS-1)
    game_over = False

    while not game_over:
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}'s turn.")

        col = get_player_choice()

        if is_valid_column(board, col):
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
                current_player_index = (current_player_index + 1) % NUM_PLAYERS

            print_board(board)
        else:
            print(f"Column {COLUMN_LABELS[col]} is full. Choose another.")

if __name__ == "__main__":
    main()
