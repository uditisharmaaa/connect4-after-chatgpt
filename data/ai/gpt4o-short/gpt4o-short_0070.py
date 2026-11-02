import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
PLAYER_COUNT = 5  # You can set this between 2 and 5

def clear_screen():
    os.system('clear')  # Use 'cls' if you're running this on Windows

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    print('  A B C D E F G')
    for row in board:
        print('|' + '|'.join(row) + '|')

def is_valid_column(column):
    return column in 'ABCDEFG'

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal locations for a win
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if (board[r][c] == piece and
                board[r][c + 1] == piece and
                board[r][c + 2] == piece and
                board[r][c + 3] == piece):
                return True

    # Check vertical locations for a win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if (board[r][c] == piece and
                board[r + 1][c] == piece and
                board[r + 2][c] == piece and
                board[r + 3][c] == piece):
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if (board[r][c] == piece and
                board[r + 1][c + 1] == piece and
                board[r + 2][c + 2] == piece and
                board[r + 3][c + 3] == piece):
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if (board[r][c] == piece and
                board[r - 1][c + 1] == piece and
                board[r - 2][c + 2] == piece and
                board[r - 3][c + 3] == piece):
                return True
    return False

def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    clear_screen()
    board = create_board()
    game_over = False

    # Select random first player
    turn = random.randint(0, PLAYER_COUNT - 1)

    while not game_over:
        clear_screen()
        print_board(board)
        print(f"Player {PLAYER_SYMBOLS[turn]}'s turn.")

        col_input = input("Select a column (A-G): ").strip().upper()
        
        if not is_valid_column(col_input):
            print("Invalid column. Please choose from A-G.")
            continue

        col = ord(col_input) - ord('A')

        row = get_next_open_row(board, col)
        if row is None:
            print("Column full. Choose another column.")
            continue

        drop_piece(board, row, col, PLAYER_SYMBOLS[turn])

        if winning_move(board, PLAYER_SYMBOLS[turn]):
            clear_screen()
            print_board(board)
            print(f"Player {PLAYER_SYMBOLS[turn]} wins!")
            game_over = True

        elif is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            game_over = True

        turn = (turn + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
