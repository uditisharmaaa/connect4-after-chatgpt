import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + "   ".join(COL_LABELS))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")
        
def get_num_players():
    while True:
        try:
            num = int(input("Enter number of players (2-5): "))
            if 2 <= num <= 5:
                return num
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_valid_column(board):
    while True:
        col = input("Choose a column (A-G): ").upper()
        if col in COL_LABELS:
            col_index = COL_LABELS.index(col)
            if board[0][col_index] == ' ':
                return col_index
            else:
                print(f"Column {col} is full. Choose another column.")
        else:
            print("Invalid column. Please choose from A to G.")

def drop_piece(board, col, piece):
    # Start from the bottom row, drop piece where empty
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = piece
            return row, col

def check_winner(board, piece, row, col):
    # Directions: horizontal, vertical, diagonal /
    def count_continuous(r_step, c_step):
        count = 0
        r, c = row + r_step, col + c_step
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == piece:
            count += 1
            r += r_step
            c += c_step
        return count

    # Check horizontal
    total = 1 + count_continuous(0, -1) + count_continuous(0, 1)
    if total >= 4:
        return True

    # Check vertical
    total = 1 + count_continuous(-1, 0) + count_continuous(1, 0)
    if total >= 4:
        return True

    # Check diagonal \
    total = 1 + count_continuous(-1, -1) + count_continuous(1, 1)
    if total >= 4:
        return True

    # Check diagonal /
    total = 1 + count_continuous(-1, 1) + count_continuous(1, -1)
    if total >= 4:
        return True

    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_num_players()
    players = PLAYER_MARKERS[:num_players]

    board = create_board()
    current_player_index = random.randrange(num_players)

    while True:
        clear_screen()
        print_board(board)
        player_piece = players[current_player_index]
        print(f"Player {player_piece}'s turn")

        col = get_valid_column(board)
        row, col = drop_piece(board, col, player_piece)

        # Check win
        if check_winner(board, player_piece, row, col):
            clear_screen()
            print_board(board)
            print(f"Player {player_piece} wins! Congratulations!")
            break

        # Check draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! Well played all.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
