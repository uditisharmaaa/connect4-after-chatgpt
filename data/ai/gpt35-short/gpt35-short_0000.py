import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COL_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS*2+1))

def get_player_count():
    while True:
        try:
            count = int(input(f"Enter number of players (2 to 5): "))
            if 2 <= count <= 5:
                return count
        except:
            pass
        print("Invalid input. Please enter a number between 2 and 5.")

def get_move(player, board):
    while True:
        col = input(f"Player {player} Enter column (A-G): ").upper().strip()
        if col in COL_LABELS:
            col_idx = COL_LABELS.index(col)
            # Check if column is full
            if board[0][col_idx] == ' ':
                return col_idx
            else:
                print("Column is full. Choose another column.")
        else:
            print("Invalid column. Choose a column A-G.")

def place_piece(board, col, symbol):
    # Drop piece from bottom, find first free spot from bottom
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row, col

def check_winner(board, symbol):
    # Check horizontal, vertical, diagonal (both ways)
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != symbol:
                continue

            # Horizontal right
            if c + 3 < COLS:
                if all(board[r][c+i] == symbol for i in range(4)):
                    return True

            # Vertical down
            if r + 3 < ROWS:
                if all(board[r+i][c] == symbol for i in range(4)):
                    return True

            # Diagonal down-right
            if r + 3 < ROWS and c + 3 < COLS:
                if all(board[r+i][c+i] == symbol for i in range(4)):
                    return True

            # Diagonal down-left
            if r + 3 < ROWS and c - 3 >= 0:
                if all(board[r+i][c-i] == symbol for i in range(4)):
                    return True

    return False

def check_draw(board):
    # Draw if no spaces at top row
    return all(cell != ' ' for cell in board[0])

def main():
    clear_screen()
    print("Welcome to Connect 4!")

    player_count = get_player_count()
    players = PLAYER_SYMBOLS[:player_count]

    # Random first player index
    current_player_idx = random.randint(0, player_count - 1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        player_symbol = players[current_player_idx]
        print(f"Player turn: {player_symbol}")

        col = get_move(player_symbol, board)
        row, col_played = place_piece(board, col, player_symbol)

        # Check for win
        if check_winner(board, player_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {player_symbol} wins! Congratulations!")
            break
        
        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % player_count

if __name__ == "__main__":
    main()
