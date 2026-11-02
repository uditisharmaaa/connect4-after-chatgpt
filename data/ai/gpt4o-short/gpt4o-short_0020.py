import random
import os

# Constants for easy configuration
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear')  # Use 'cls' if you're on Windows

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (2 * COLUMNS + 1))

def is_valid_column(board, column):
    # Returns True if the column is within range and not full
    return 0 <= column < COLUMNS and board[0][column] == ' '

def next_open_row(board, column):
    # Returns the next open row index for the column, -1 if full
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            return row
    return -1

def drop_piece(board, row, column, piece):
    board[row][column] = piece

def check_for_win(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def play_game(num_players):
    board = create_board(ROWS, COLUMNS)
    game_over = False
    turn = random.randint(0, num_players - 1)

    while not game_over:
        print_board(board)
        print(f"Player {PLAYER_SYMBOLS[turn]}'s turn")

        column_input = input("Choose a column (A-G): ").upper()
        if column_input in COLUMN_LABELS:
            column = COLUMN_LABELS.index(column_input)
        else:
            print("Invalid input. Please select a column from A-G.")
            continue

        if is_valid_column(board, column):
            row = next_open_row(board, column)
            drop_piece(board, row, column, PLAYER_SYMBOLS[turn])

            if check_for_win(board, PLAYER_SYMBOLS[turn]):
                print_board(board)
                print(f"Player {PLAYER_SYMBOLS[turn]} wins!")
                game_over = True
            elif is_draw(board):
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                turn += 1
                turn %= num_players
        else:
            print("Column is full. Try another column.")

if __name__ == '__main__':
    num_players = input("Enter number of players (2-5): ")
    if num_players.isdigit():
        num_players = int(num_players)
        if 2 <= num_players <= 5:
            play_game(num_players)
        else:
            print("Invalid number of players. Please enter between 2 and 5.")
    else:
        print("Invalid input. Please enter a number between 2 and 5.")
