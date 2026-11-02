import os
import random

ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def is_valid_column(board, col):
    return 0 <= col < COLS and board[0][col] == ' '

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def drop_piece(board, row, col, piece):
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

def is_board_full(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def get_player_count():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Enter an integer.")

def get_player_move(player, board):
    while True:
        move = input(f"Player {player} turn - choose column (A-G): ").strip().upper()
        if move in COLUMN_LABELS:
            col = COLUMN_LABELS.index(move)
            if is_valid_column(board, col):
                return col
            else:
                print("That column is full. Choose another.")
        else:
            print("Invalid column. Choose a letter from A to G.")

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    player_count = get_player_count()
    players = PLAYER_SYMBOLS[:player_count]

    board = create_board()
    turn = random.randint(0, player_count - 1)  # random first player

    while True:
        clear_screen()
        print_board(board)
        current_player = players[turn]
        col = get_player_move(current_player, board)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, current_player)

        if winning_move(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("The board is full! It's a draw!")
            break
        
        turn = (turn + 1) % player_count

if __name__ == "__main__":
    main()
