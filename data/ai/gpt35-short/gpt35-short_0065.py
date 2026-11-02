import os
import random

ROWS = 6
COLS = 7
COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Set number of players here (2 to 5)
NUM_PLAYERS = 3  # example: 3 players
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COLUMNS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def get_column_index(col):
    col = col.upper()
    if col in COLUMNS:
        return COLUMNS.index(col)
    return -1

def is_valid_column(board, col):
    return board[0][col] == ' '

def drop_piece(board, col, piece):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = piece
            return row, col

def check_winner(board, piece):
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
    # Check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    # Check diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS -1)

    while True:
        clear_screen()
        print_board(board)
        player = PLAYERS[current_player_index]
        print(f"Player {player}'s turn.")

        col_input = input(f"Choose a column (A-G): ").strip()
        col = get_column_index(col_input)
        if col == -1:
            print("Invalid column. Please enter A-G.")
            input("Press Enter to continue...")
            continue
        if not is_valid_column(board, col):
            print("Column is full, choose another one.")
            input("Press Enter to continue...")
            continue

        drop_piece(board, col, player)

        if check_winner(board, player):
            clear_screen()
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("Game over!")

if __name__ == "__main__":
    main()
