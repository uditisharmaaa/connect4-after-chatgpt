import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMNS_LABELS = "ABCDEFG"
PLAYERS_PIECES = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COLUMNS_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (2 * COLS + 1))

def is_valid_column(col):
    return 0 <= col < COLS

def is_column_full(board, col):
    return board[0][col] != ' '

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    # Check positively sloped diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    # Check negatively sloped diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    return False

def board_full(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def get_num_players():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Number of players must be between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer between 2 and 5.")

def get_player_move(player, piece):
    while True:
        move = input(f"Player {piece}, choose column (A-G): ").strip().upper()
        if move in COLUMNS_LABELS:
            col = COLUMNS_LABELS.index(move)
            return col
        else:
            print("Invalid column. Please enter a letter between A and G.")

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_num_players()
    players = PLAYERS_PIECES[:num_players]

    board = create_board()
    turn = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)

        piece = players[turn]
        col = get_player_move(turn, piece)

        if is_column_full(board, col):
            print(f"Column {COLUMNS_LABELS[col]} is full. Please pick another column.")
            input("Press Enter to continue...")
            continue

        row = get_next_open_row(board, col)
        drop_piece(board, row, col, piece)

        if winning_move(board, piece):
            clear_screen()
            print_board(board)
            print(f"Player {piece} wins! Congratulations!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        turn = (turn + 1) % num_players

if __name__ == "__main__":
    main()
