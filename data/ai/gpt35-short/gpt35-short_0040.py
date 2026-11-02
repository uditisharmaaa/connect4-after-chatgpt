import random
import os

ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COL_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def get_player_count():
    while True:
        try:
            count = int(input(f"Enter number of players (2-{len(PLAYERS_SYMBOLS)}): "))
            if 2 <= count <= len(PLAYERS_SYMBOLS):
                return count
            else:
                print(f"Please enter a number between 2 and {len(PLAYERS_SYMBOLS)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_move(player_symbol, board):
    while True:
        move = input(f"Player {player_symbol}, choose column (A-G): ").upper()
        if move not in COL_LABELS:
            print("Invalid column. Please enter a letter from A to G.")
            continue
        col = COL_LABELS.index(move)
        if board[0][col] != ' ':
            print("Column is full. Pick another one.")
            continue
        return col

def make_move(board, col, player_symbol):
    # Place token in the lowest empty row in the column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_symbol
            return row, col

def check_winner(board, player_symbol, row, col):
    # Check all directions: horizontal, vertical, diagonal /
    def count_dir(r, c, dr, dc):
        count = 0
        nr, nc = r + dr, c + dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == player_symbol:
            count += 1
            nr += dr
            nc += dc
        return count

    # Check horizontal
    total = 1 + count_dir(row, col, 0, 1) + count_dir(row, col, 0, -1)
    if total >= 4:
        return True
    # Check vertical
    total = 1 + count_dir(row, col, 1, 0) + count_dir(row, col, -1, 0)
    if total >= 4:
        return True
    # Check diagonal \
    total = 1 + count_dir(row, col, 1, 1) + count_dir(row, col, -1, -1)
    if total >= 4:
        return True
    # Check diagonal /
    total = 1 + count_dir(row, col, 1, -1) + count_dir(row, col, -1, 1)
    if total >= 4:
        return True

    return False

def is_draw(board):
    # If top row is full, board is full
    return all(cell != ' ' for cell in board[0])

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    player_count = get_player_count()
    players = PLAYERS_SYMBOLS[:player_count]

    # Randomly pick first player index
    current_player_idx = random.randint(0, player_count - 1)
    
    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        player_symbol = players[current_player_idx]

        col = get_move(player_symbol, board)
        row, col = make_move(board, col, player_symbol)

        if check_winner(board, player_symbol, row, col):
            clear_screen()
            print_board(board)
            print(f"Player {player_symbol} wins! Congratulations!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        current_player_idx = (current_player_idx + 1) % player_count

if __name__ == "__main__":
    main()
