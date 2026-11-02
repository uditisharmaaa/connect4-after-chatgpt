import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("+" + "-+" * COLS)

def get_player_count():
    while True:
        try:
            count = int(input(f"Enter number of players (2-{len(PLAYER_TOKENS)}): "))
            if 2 <= count <= len(PLAYER_TOKENS):
                return count
            else:
                print(f"Please enter a number between 2 and {len(PLAYER_TOKENS)}.")
        except ValueError:
            print("Please enter a valid number.")

def get_valid_column(player):
    while True:
        col = input(f"Player {player} select column (A-G): ").upper()
        if col in COLUMN_LABELS:
            col_index = COLUMN_LABELS.index(col)
            return col_index
        else:
            print("Invalid column. Please select a column between A and G.")

def is_valid_move(board, col):
    return board[0][col] == ' '

def drop_piece(board, col, piece):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = piece
            return row, col

def check_winner(board, piece):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == piece for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == piece for i in range(4)):
                return True

    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    player_count = get_player_count()
    players = PLAYER_TOKENS[:player_count]

    board = create_board()
    current_player_idx = random.randint(0, player_count - 1)

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_player_idx]
        print(f"Player {current_player}'s turn")

        col = get_valid_column(current_player)
        if not is_valid_move(board, col):
            print("Column is full! Choose another column.")
            input("Press Enter to continue...")
            continue

        drop_piece(board, col, current_player)

        if check_winner(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        current_player_idx = (current_player_idx + 1) % player_count

if __name__ == "__main__":
    main()
